# Local Media Library companion

The Media Library uses one folder per operating-system user, shared by Chrome and the OBS browser dock on the same computer. Start the companion on every computer that needs to import or inspect files. It is a separate Python process from Django and the Vercel deployment.

Install the repository's Python dependencies, then set `GKPS_MEDIA_ALLOWED_ORIGINS` to the exact origin shown in the browser address bar (scheme, hostname, and optional port, without a trailing slash). For example:

```sh
GKPS_MEDIA_ALLOWED_ORIGINS=https://your-app.example python -m multimedia.local_media
```

On Windows PowerShell:

```powershell
$env:GKPS_MEDIA_ALLOWED_ORIGINS = 'https://your-app.example'
python -m multimedia.local_media
```

For local development, use the exact development origin, such as `http://127.0.0.1:8000`. Multiple exact origins may be separated by commas. The companion prints the resolved library folder and listens on `http://127.0.0.1:47863`. Keep the process running while using the Media Library. Its SQLite index is in that folder; back up the entire folder to preserve filenames and retention state along with file bytes. On restart, the existing folder and index are reused.

The browser may ask to allow local-network access to the companion. Allow it for the configured app origin. If the process is stopped or the browser blocks the connection, Media Library status shows **Unavailable** and service media entries show **Local library unavailable**. Existing service entries remain saved. The status popup reveals the actual folder path only when connected.

Imports have a 200 MB limit. Selecting a file inspects a temporary copy; saving the entry imports it into the library. The companion checks content signatures regardless of extension and uses SHA-256 of the full bytes for identity. Importing the same bytes again reuses the original library filename. Removing a file deletes only its local copy; Tata Ibadah entries stay. Unused-file cleanup runs only after a successful, complete reference inventory from Django, so a disconnected app cannot silently cause cleanup. The default retention is 30 days per computer.

The companion binds only to loopback, accepts only configured browser origins, and requires a session token for writes. Do not expose its port through a proxy or on a public network interface.
