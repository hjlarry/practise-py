import asyncio
from aiohttp import web
import pathlib
from charfinder import UnicodeNameIndex

ROW_TPL = "<tr><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>"
TEMPLATE_NAME = "http_charfinder.html"
HERE = pathlib.Path(__file__)
index = UnicodeNameIndex()
with open(HERE.parent / TEMPLATE_NAME) as tpl:
    template = tpl.read()


async def init(loop, addr, port):
    app = web.Application(loop=loop)
    app.router.add_route("GET", "/", home)
    handler = app.make_handler()
    server = await loop.create_server(handler, addr, port)
    return server.sockets[0].getsockname()


def home(request):
    query = request.GET.get("query", "").strip()
    print(f"Query:{query!r}")
    if query:
        descriptions = list(index.find_descriptions(query))
        res = "\n".join(ROW_TPL.format(**descr._asdict()) for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ""
        msg = "Enter words describing characters"
    html = template.format(query=query, result=res, message=msg)
    print(f"sending {len(descriptions)} results")
    return web.Response(content_type="text/html", text=html)


def main(addr="127.0.0.1", port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init(loop, addr, port))
    print(f"Serving on {host}, ctrl+c to stop")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("serving shut down")
    loop.close()


main()
