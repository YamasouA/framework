def application(env, start_response):
    # start_response(status, headers)
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'Hello World']

