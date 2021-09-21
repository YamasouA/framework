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

class App:
    def __init__(self):
        self.router = Router()

    # routeデコレータを使ってコールバック関数にHTTPメソッドと正規表現でかかれたパスを割り当ててできるようにする
    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def __call__(self, env, start_response):
        method = env['REQUEST_METHOD'].upper()
        path = env['PATH_INFO'] or '/'
        callback, kwargs = self.router.match(method, path)
        return callback(env, start_response, **kwargs)
