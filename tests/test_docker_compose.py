"""Guards for the local Docker Compose stack (spec 002).

These pin the port rules so the stack cannot drift back onto the crowded
well-known range, and keep ``.env.example`` in step with the compose defaults.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml
from django.test import SimpleTestCase

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPOSE_FILE = REPO_ROOT / "docker-compose.yml"
ENV_EXAMPLE = REPO_ROOT / ".env.example"

# IANA dynamic/private range: random, unlikely to collide with other apps.
DYNAMIC_PORT_MIN = 49152
DYNAMIC_PORT_MAX = 65535
WELL_KNOWN_PORTS = {8000, 5432}

# Compose short syntax with an overridable default host port:
#   "${WEB_PORT:-63404}:8000"
_PORT_SPEC = re.compile(
    r"^\$\{(?P<var>[A-Z_]+):-(?P<default>\d+)\}:(?P<container>\d+)$"
)


def parse_published_port(spec: str) -> tuple[int, int]:
    """Return ``(host_default, container_port)`` from a compose port entry."""
    match = _PORT_SPEC.match(spec)
    if match is None:
        raise AssertionError(f"unexpected published port spec: {spec!r}")
    return int(match.group("default")), int(match.group("container"))


class DockerComposePortRulesTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not COMPOSE_FILE.exists():
            raise AssertionError("docker-compose.yml is missing")
        cls.compose = yaml.safe_load(COMPOSE_FILE.read_text(encoding="utf-8"))

    def _published(self, service: str) -> tuple[int, int]:
        ports = self.compose["services"][service]["ports"]
        return parse_published_port(ports[0])

    def test_services_present(self):
        services = self.compose.get("services", {})
        self.assertIn("web", services)
        self.assertIn("db", services)
        self.assertIn("media", services)

    def test_published_ports_avoid_well_known_range(self):
        published = {}
        for service in ("web", "db"):
            host, _ = self._published(service)
            published[service] = host
            self.assertGreaterEqual(
                host,
                DYNAMIC_PORT_MIN,
                f"{service} publishes {host}, below the IANA dynamic range",
            )
            self.assertLessEqual(
                host,
                DYNAMIC_PORT_MAX,
                f"{service} publishes {host}, above the IANA dynamic range",
            )
            self.assertNotIn(
                host,
                WELL_KNOWN_PORTS,
                f"{service} publishes the well-known port {host}",
            )
        self.assertNotEqual(
            published["web"],
            published["db"],
            "web and db must publish different host ports",
        )

    def test_container_ports_are_conventional(self):
        _, web_container = self._published("web")
        _, db_container = self._published("db")
        self.assertEqual(web_container, 8000)
        self.assertEqual(db_container, 5432)

    def test_media_companion_uses_private_loopback_port_and_named_volume(self):
        media = self.compose["services"]["media"]
        self.assertEqual(media["ports"], ["127.0.0.1:63174:63174"])
        self.assertEqual(media["restart"], "unless-stopped")
        self.assertEqual(media["environment"]["GKPS_MEDIA_LIBRARY_ROOT"], "/var/lib/gkps-media")
        self.assertEqual(
            media["volumes"], ["media_library_data:/var/lib/gkps-media"]
        )
        self.assertNotIn(".:/app", media["volumes"])
        self.assertIn("media_library_data", self.compose["volumes"])

    def test_media_companion_allowlist_uses_required_production_and_both_web_origins(self):
        origins = self.compose["services"]["media"]["environment"]["GKPS_MEDIA_ALLOWED_ORIGINS"]
        self.assertIn("${GKPS_MEDIA_PRODUCTION_ORIGIN:?", origins)
        self.assertIn("http://localhost:${WEB_PORT:-63404}", origins)
        self.assertIn("http://127.0.0.1:${WEB_PORT:-63404}", origins)

    def test_media_companion_endpoint_is_consistent_in_browser_and_python_clients(self):
        sources = (
            REPO_ROOT / "multimedia/local_media.py",
            REPO_ROOT / "static/web/media-library.js",
            REPO_ROOT / "static/web/media-entry.js",
            REPO_ROOT / "static/web/media-stage.js",
        )
        for source in sources:
            text = source.read_text(encoding="utf-8")
            self.assertIn("63174", text, f"{source.name} must use the companion port")
            self.assertNotIn("47863", text, f"{source.name} retains the old companion port")

    def test_env_example_matches_compose_defaults(self):
        self.assertTrue(ENV_EXAMPLE.exists(), ".env.example is missing")
        text = ENV_EXAMPLE.read_text(encoding="utf-8")
        web_default, _ = self._published("web")
        db_default, _ = self._published("db")
        self.assertIn(f"WEB_PORT={web_default}", text)
        self.assertIn(f"DB_PORT={db_default}", text)
        self.assertIn("GKPS_MEDIA_PRODUCTION_ORIGIN=", text)
