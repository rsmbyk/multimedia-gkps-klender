# Contracts — spec 166

The companion exposes an HTTP surface and the product reads it. This slice changes nothing it
returns; the contract below is what a reviewer checks the diff against.

## `GET /v1/slides/<sha256>` — the converted deck

| Aspect | Contract |
| --- | --- |
| Auth / origin | unchanged: `Host` must be the loopback port, `Origin` must be in `GKPS_MEDIA_ALLOWED_ORIGINS`, otherwise `403 {"error": "Origin is not allowed."}` |
| Success | `200`, `Content-Type: application/pdf`, body is the derivative |
| Unknown / non-slide file | `404 {"error": "PowerPoint unavailable on this computer."}` |
| No LibreOffice | `404 {"error": "PowerPoint conversion is unavailable."}` |
| Conversion failed | `404 {"error": "PowerPoint conversion failed."}` |
| Conversion timed out | `404 {"error": "PowerPoint conversion timed out."}` |
| Wrong suffix | `404 {"error": "PowerPoint conversion did not produce a PDF."}` |
| Cache | unchanged: `Cache-Control: no-store` with the rest of the JSON replies; the file reply keeps its own headers |

The body differs — that is the point of the slice — and nothing else in this row may.

## `GET /v1/status`, `GET /v1/files`, `GET /v1/transfers`, `POST`/`DELETE` on `/v1/files`

Unchanged in path, method, status, payload shape and header set. The font mapping, the conversion and
the derivative key are invisible to them.

## Environment

| Variable | Contract |
| --- | --- |
| `GKPS_MEDIA_LIBRARY_ROOT` | unchanged |
| `GKPS_MEDIA_SERVER_ORIGIN`, `GKPS_MEDIA_ALLOWED_ORIGINS` | unchanged |
| `GKPS_FONTS_DIR` | **new, optional** — the host directory mounted at `/usr/share/fonts/operator`. Unset means compose's default path; a missing directory means no operator fonts. It is never read by the application. |

## Internal, but shared

`convert_slides(input_path, output_path)` keeps its signature and its behaviour (it writes the PDF at
`output_path`; it raises `InvalidMedia` on timeout and `CalledProcessError` on a non-zero exit), because
the tests pass their own converter through the same seam.
