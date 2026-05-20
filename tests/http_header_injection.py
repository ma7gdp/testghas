from flask import Response, request


def header_injection():
    value = request.args.get("value")
    resp = Response("OK")
    resp.headers["X-Data"] = value
    return resp
