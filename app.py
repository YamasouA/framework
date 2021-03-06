from router import Router
from request import Request


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
        request = Request(env)
        callback, kwargs = self.route.match(request.method, request.path)
        return callback(env, start_response, **kwargs)
