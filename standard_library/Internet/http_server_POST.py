from http.server import BaseHTTPRequestHandler, HTTPServer
import io
import cgi


class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 分析提交表单的数据
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"],
            },
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/plain;charset=utf-8")
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile, encoding="utf-8", line_buffering=False, write_through=True
        )
        out.write(f'Client: {self.client_address} \n')
        out.write('User-agent: {} \n'.format(self.headers['user-agent']))
        out.write(f'Path: {self.path} \n')
        out.write('Form data: \n')

        for field in form.keys():
            field_item = form[field]
            # 如果字段中有上传文件的字段
            if field_item.filename:
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                out.write(f'\t Uploaded {field} as {field_item.filename!r} ({file_len} bytes)\n')
            else:
                out.write(f'\t {field} = {form[field].value}')
        # 将编码 wrapper 到底层缓冲的连接断开，使得将 wrapper 删除时，并不关闭仍被服务器使用 socket 
        out.detach()



server = HTTPServer(("127.0.0.1", 8081), PostHandler)
print("server run....")
server.serve_forever()
