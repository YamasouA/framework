def application(env, start_response):
    # start_response(status, headers)
    path = env['PATH_INFO']
    if path == '/':
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [b'Hello World']
    elif path == '/foo':
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [b'foo']
    else:
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [b'404 Not Found']

