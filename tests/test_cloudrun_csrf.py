"""Regression for the Cloud Run CSRF origin failure (spec 251).

A TLS-terminating proxy makes Django see plain HTTP unless SECURE_PROXY_SSL_HEADER says
otherwise; the browser's HTTPS Origin is then compared with an http:// host and every
write is rejected. The probe view has no database and writes nothing.
"""
from django.http import HttpResponse
from django.test import Client, SimpleTestCase, override_settings
from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie

HOST = "multimedia-gkps-klender-73206048678.asia-southeast2.run.app"


@ensure_csrf_cookie
def write_probe(request):
    return HttpResponse("write accepted")


urlpatterns = [path("write/", write_probe, name="write")]


@override_settings(ROOT_URLCONF=__name__, ALLOWED_HOSTS=["*"])
class CloudRunCsrfTests(SimpleTestCase):
    def post_with_browser_origin(self):
        client = Client(enforce_csrf_checks=True)
        client.get("/write/", HTTP_HOST=HOST, SERVER_PORT=8080)
        token = client.cookies["csrftoken"].value
        return client.post(
            "/write/",
            {"csrfmiddlewaretoken": token},
            HTTP_HOST=HOST,
            HTTP_ORIGIN=f"https://{HOST}",
            HTTP_X_FORWARDED_PROTO="https",
            SERVER_PORT=8080,
        )

    def test_a_forwarded_https_request_is_accepted(self):
        # Cloud Run shape: HTTPS Origin, forwarded proto, port 8080 behind the proxy.
        response = self.post_with_browser_origin()
        self.assertEqual(response.status_code, 200, response.content.decode()[:300])

    def test_without_the_proxy_header_the_https_origin_is_rejected(self):
        # The fix must not turn CSRF off: without the setting the same POST is still 403.
        with override_settings(SECURE_PROXY_SSL_HEADER=None):
            response = self.post_with_browser_origin()
        self.assertEqual(response.status_code, 403)
