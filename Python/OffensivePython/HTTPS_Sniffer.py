#/usr/bin/env python3

from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    """
    Esta función se ejecuta cada vez que se intercepta una solicitud HTTP/HTTPS.
    """
    print(f"🔍 [REQUEST] {flow.request.method} {flow.request.pretty_url}")
    print(f"   🔐 HTTPS: {flow.request.scheme == 'https'}")
    if flow.request.content:
        print(f"   📦 Body: {flow.request.content.decode('utf-8', errors='ignore')}")

def response(flow: http.HTTPFlow) -> None:
    """
    Esta función se ejecuta cada vez que se intercepta una respuesta HTTP/HTTPS.
    """
    print(f"✅ [RESPONSE] {flow.response.status_code} {flow.request.pretty_url}")
    if flow.response.content:
        print(f"   📄 Response Body: {flow.response.content.decode('utf-8', errors='ignore')[:500]}...")