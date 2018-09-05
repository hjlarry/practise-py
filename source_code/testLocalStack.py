from .FlaskOrigin import Flask, _request_ctx_stack, redirect, url_for
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
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
app1.run(port=5002, threaded=True)


 * Running on http://localhost:5002/ (Press CTRL+C to quit)
{<greenlet.greenlet object at 0x10504aaf8>: {'stack': [<flask_me._RequestContext object at 0x1051b6780>]}} 1
{<greenlet.greenlet object at 0x10504aaf8>: {'stack': [<flask_me._RequestContext object at 0x1051b6780>]}, <greenlet.greenlet object at 0x10504ab90>: {'stack': [<flask_me._RequestContext object at 0x1051b6c18>]}} 3
{<greenlet.greenlet object at 0x10504aaf8>: {'stack': [<flask_me._RequestContext object at 0x1051b6780>]}, <greenlet.greenlet object at 0x10504ab90>: {'stack': [<flask_me._RequestContext object at 0x1051b6c18>]}} 2
{<greenlet.greenlet object at 0x10504ab90>: {'stack': [<flask_me._RequestContext object at 0x1051b6c18>]}} 4
'''

'''
run_simple(hostname='127.0.0.1', port=5002, application=application, threaded=True)
 * Running on http://127.0.0.1:5002/ (Press CTRL+C to quit)
{<greenlet.greenlet object at 0x11052ba60>: {'stack': [<flask_me._RequestContext object at 0x110694c50>]}} 1
{<greenlet.greenlet object at 0x11052ba60>: {'stack': [<flask_me._RequestContext object at 0x110694c50>]}, <greenlet.greenlet object at 0x11052baf8>: {'stack': [<flask_me._RequestContext object at 0x1106ab198>]}} 3
{<greenlet.greenlet object at 0x11052ba60>: {'stack': [<flask_me._RequestContext object at 0x110694c50>]}, <greenlet.greenlet object at 0x11052baf8>: {'stack': [<flask_me._RequestContext object at 0x1106ab198>]}} 2
127.0.0.1 - - [05/Sep/2018 13:20:49] "GET / HTTP/1.1" 200 -
{<greenlet.greenlet object at 0x11052baf8>: {'stack': [<flask_me._RequestContext object at 0x1106ab198>]}} 4
127.0.0.1 - - [05/Sep/2018 13:20:56] "GET /admin/1 HTTP/1.1" 200 -
'''