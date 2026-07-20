#!/usr/bin/env python3
"""Deploy sca-timer/www to Netlify using Chrome session cookies."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WWW = ROOT / "www"


def ensure_browser_cookie3():
    try:
        import browser_cookie3  # noqa: F401
        return
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "browser-cookie3"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def load_cookies() -> dict[str, str]:
    import browser_cookie3

    cookies: dict[str, str] = {}
    for domain in ("netlify.com", ".netlify.com", "app.netlify.com"):
        try:
            cj = browser_cookie3.chrome(domain_name=domain)
            for c in cj:
                cookies[c.name] = c.value
        except Exception as e:
            print(f"cookie warn {domain}: {type(e).__name__}: {e}", file=sys.stderr)
    return cookies


def zip_www(dest: Path) -> None:
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in WWW.rglob("*"):
            if path.is_file() and path.name != ".DS_Store":
                zf.write(path, path.relative_to(WWW).as_posix())


def main() -> int:
    ensure_browser_cookie3()
    cookies = load_cookies()
    print("cookie_names:", sorted(cookies.keys()))
    if not cookies:
        print("NO_COOKIES", file=sys.stderr)
        return 2

    # Prefer nf_jwt / _nf-auth style tokens if present
    auth_header = None
    for key in ("nf_jwt", "nf-jwt", "nf_token", "token", "jwt"):
        if key in cookies and cookies[key]:
            auth_header = f"Bearer {cookies[key]}"
            print(f"using cookie auth key={key}")
            break

    import urllib.request

    cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items())
    with tempfile.TemporaryDirectory() as td:
        zip_path = Path(td) / "site.zip"
        zip_www(zip_path)
        data = zip_path.read_bytes()
        print(f"zip_bytes={len(data)}")

        req = urllib.request.Request(
            "https://api.netlify.com/api/v1/sites",
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/zip",
                "Cookie": cookie_header,
                **({"Authorization": auth_header} if auth_header else {}),
                "User-Agent": "sca-timer-deploy/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read().decode()
                print("status", resp.status)
                print(body[:4000])
                info = json.loads(body)
                url = info.get("ssl_url") or info.get("url")
                print("SHARE_URL", url)
                (ROOT / "NETLIFY_URL.txt").write_text(url + "\n", encoding="utf-8")
                return 0
        except Exception as e:
            err = getattr(e, "read", lambda: b"")()
            print("DEPLOY_FAIL", e, file=sys.stderr)
            if err:
                print(err.decode()[:2000], file=sys.stderr)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
