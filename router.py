import re

def http404(env, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'404 Not Found']

def http405(env, start_response):
    start_response('405 Method Not Allowed', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'405 Method Not Allowed']

class Router:
    def __init__(self):
        self.routes = []

    # 各コールバック関数がどのURLパス・HTTPメソッドに紐づくかを登録
    def add(self, method, path, callback):
        self.routes.append({
            'method':method,
            'path': path,
            'callback': callback
        })

    # 受け取ったリクエストのパスとHTTPメソッドの情報をもとに登録したコールバック関数とURL変数を返す
    def match(self, method, path):
        error_callback = http404
        for r in self.routes:
            matched = re.compile(r['path']).match(path)
            if not matched:
                continue
            error_callback = http405
            url_vars = matched.groupdict()
            if r['method'] == method:
                return r['callback'], url_vars
        return error_callback, {}
