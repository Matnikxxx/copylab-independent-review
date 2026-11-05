#!/usr/bin/env python3
"""Serve the CopyLab review ZIP as a clickable download.

Binds 0.0.0.0 so the sandbox preview proxy can reach it.
Serves an index page with the download link and the published SHA-256.
"""
import hashlib
import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path("/home/user/copylab-independent-review/review-deliverables")
ZIP = ROOT / "COPYLAB-INDEPENDENT-REVIEW-ad8470c71a4421994cb8514ae7d2139adf1f086d.zip"
PORT = 8000


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


SHA = sha256_of(ZIP) if ZIP.exists() else "0" * 64


INDEX = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CopyLab — independent review package</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         max-width: 46rem; margin: 3rem auto; padding: 0 1.25rem; }}
  h1 {{ font-size: 1.5rem; margin-bottom: .25rem; }}
  .sub {{ opacity: .7; margin-top: 0; }}
  .card {{ border: 1px solid rgba(128,128,128,.35); border-radius: 10px;
           padding: 1.25rem 1.4rem; margin: 1.75rem 0; }}
  a.dl {{ display: inline-block; background: #2563eb; color: #fff; text-decoration: none;
          padding: .8rem 1.4rem; border-radius: 8px; font-weight: 600; }}
  a.dl:hover {{ background: #1d4ed8; }}
  code {{ background: rgba(128,128,128,.16); padding: .15rem .4rem; border-radius: 4px;
          font-size: .87em; word-break: break-all; }}
  .warn {{ border-left: 4px solid #d97706; padding: .6rem 0 .6rem 1rem; margin: 1.5rem 0;
           background: rgba(217,119,6,.08); }}
  dt {{ font-weight: 600; margin-top: .6rem; }} dd {{ margin: 0 0 .2rem 0; }}
</style>
</head>
<body>
<h1>CopyLab — independent review package</h1>
<p class="sub">Built from frozen commit <code>ad8470c</code> (D-12)</p>

<div class="card">
  <a class="dl" href="/download" download>Download ZIP &nbsp;·&nbsp; 1.4 MB</a>
  <dl>
    <dt>File</dt><dd><code>{html.escape(ZIP.name)}</code></dd>
    <dt>Size</dt><dd>1.4 MB &nbsp;·&nbsp; 193 files</dd>
    <dt>SHA-256</dt><dd><code>{SHA}</code></dd>
  </dl>
</div>

<div class="warn">
  <strong>Review only.</strong> Phase 0 is <strong>NOT SATISFIED</strong> and G1–G5 are
  <strong>NOT AUTHORISED</strong>. CopyLab is strictly paper-only: no live trading, no
  credentials, no runtime database access, no deployment.
</div>

<p>Verify after download:</p>
<pre><code>sha256sum {html.escape(ZIP.name)}
unzip -q {html.escape(ZIP.name)}
cd COPYLAB-INDEPENDENT-REVIEW-ad8470c71a4421994cb8514ae7d2139adf1f086d
sha256sum -c SHA256SUMS.txt    # expect 190/190 OK</code></pre>

<p>Then read <code>README.md</code>, <code>VERIFY.md</code>, and
<code>EXCLUDED_ITEMS.md</code>, in that order.</p>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    server_version = "CopyLabReview/1.0"

    def _send(self, code: int, body: bytes, ctype: str, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        path = unquote(self.path.split("?")[0])

        if path in ("/", "/index.html"):
            body = INDEX.encode()
            self._send(200, body, "text/html; charset=utf-8")

        elif path in ("/download", "/" + ZIP.name):
            if not ZIP.exists():
                self._send(404, b"ZIP not found", "text/plain; charset=utf-8")
                return
            data = ZIP.read_bytes()
            self._send(
                200, data, "application/zip",
                {"Content-Disposition": f'attachment; filename="{ZIP.name}"'},
            )

        elif path == "/ZIP-SHA256.txt":
            p = ROOT / "ZIP-SHA256.txt"
            self._send(200, p.read_bytes() if p.exists() else b"",
                       "text/plain; charset=utf-8")

        elif path == "/healthz":
            self._send(200, b"ok", "text/plain; charset=utf-8")

        else:
            self._send(404, b"Not found", "text/plain; charset=utf-8")

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)


if __name__ == "__main__":
    print(f"serving {ZIP.name} ({ZIP.stat().st_size if ZIP.exists() else 0} bytes)", flush=True)
    print(f"sha256 {SHA}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
