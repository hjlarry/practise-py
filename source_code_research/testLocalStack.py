from FlaskOrigin import Flask, _request_ctx_stack, redirect, url_for
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from werkzeug.test import create_environ
import time

app1 = Flask(__name__)
app2 = Flask(__name__)


@app1.route('/')
def index():
    print(_request_ctx_stack._local.__storage__, 1)
    time.sleep(5)
    print(_request_ctx_stack._local.__storage__, 2)
    return 'ss'


@app2.route('/1')
def index1():
    print(_request_ctx_stack._local.__storage__, 3)
    time.sleep(10)
    print(_request_ctx_stack._local.__storage__, 4)
    return 'ss1'


application = DispatcherMiddleware(app1, {
    '/admin': app2
})

'''
EXECUTE:
app1.run(port=5002, threaded=True)

RESULT:
 * Running on http://localhost:5002/ (Press CTRL+C to quit)
{<greenlet.greenlet object at 0x10504aaf8>: {'stack': [<flask_me._RequestContext object at 0x1051b6780>]}} 1
{<greenlet.greenlet object at 0x10504aaf8>: {'stack': [<flask_me._RequestContext object at 0x1051b6780>]}, <greenlet.greenlet object at 0x10504ab90>: {'stack': [<flask_me._RequestContext object at 0x1051b6c18>]}} 3
{<greenlet.greenlet object at 0x10504aaf8>: {'stack': [<flask_me._RequestContext object at 0x1051b6780>]}, <greenlet.greenlet object at 0x10504ab90>: {'stack': [<flask_me._RequestContext object at 0x1051b6c18>]}} 2
{<greenlet.greenlet object at 0x10504ab90>: {'stack': [<flask_me._RequestContext object at 0x1051b6c18>]}} 4
'''

'''
EXECUTE:
run_simple(hostname='127.0.0.1', port=5002, application=application, threaded=True)

RESULT:
 * Running on http://127.0.0.1:5002/ (Press CTRL+C to quit)
{<greenlet.greenlet object at 0x11052ba60>: {'stack': [<flask_me._RequestContext object at 0x110694c50>]}} 1
{<greenlet.greenlet object at 0x11052ba60>: {'stack': [<flask_me._RequestContext object at 0x110694c50>]}, <greenlet.greenlet object at 0x11052baf8>: {'stack': [<flask_me._RequestContext object at 0x1106ab198>]}} 3
{<greenlet.greenlet object at 0x11052ba60>: {'stack': [<flask_me._RequestContext object at 0x110694c50>]}, <greenlet.greenlet object at 0x11052baf8>: {'stack': [<flask_me._RequestContext object at 0x1106ab198>]}} 2
127.0.0.1 - - [05/Sep/2018 13:20:49] "GET / HTTP/1.1" 200 -
{<greenlet.greenlet object at 0x11052baf8>: {'stack': [<flask_me._RequestContext object at 0x1106ab198>]}} 4
127.0.0.1 - - [05/Sep/2018 13:20:56] "GET /admin/1 HTTP/1.1" 200 -
'''

'''
EXECUTE:
with app1.request_context(create_environ()):
    with app1.request_context(create_environ()):
        print(_request_ctx_stack._local.__storage__, 99)
        
RESULT:
{<greenlet.greenlet object at 0x10f70d638>: {'stack': [<FlaskOrigin._RequestContext object at 0x10fcb2080>, <FlaskOrigin._RequestContext object at 0x10fcb21d0>]}} 99
通过with可以模拟推送多个请求的情况，但实际场景没想到如何模拟
'''

'''
from flask import Flask, current_app, _app_ctx_stack
import logging

app = Flask("app1")
app2 = Flask("app2")

app.config.logger = logging.getLogger("app1.logger")
app2.config.logger = logging.getLogger("app2.logger")

app.logger.addHandler(logging.FileHandler("app_log.txt"))
app2.logger.addHandler(logging.FileHandler("app2_log.txt"))

with app.app_context():
    with app2.app_context():
        try:
            print(_app_ctx_stack._local.__storage__, 9)
            raise ValueError("app2 error")
        except Exception as e:
            current_app.config.logger.exception(e)
    try:
        print(_app_ctx_stack._local.__storage__, 10)
        raise ValueError("app1 error")
    except Exception as e:
        current_app.config.logger.exception(e)


这段代码解决了为什么要用栈存储App Context

{<greenlet.greenlet object at 0x106dee6d0>: {'stack': [<flask.ctx.AppContext object at 0x107487668>, <flask.ctx.AppContext object at 0x1074876d8>]}} 9
Traceback (most recent call last):
{<greenlet.greenlet object at 0x106dee6d0>: {'stack': [<flask.ctx.AppContext object at 0x107487668>]}} 10
'''
