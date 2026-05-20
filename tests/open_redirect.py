from flask import redirect, request


def app_redirect():
    url = request.args.get('next')
    return redirect(url)
