# python3 -m uvicorn http_mojifinder:app
from pathlib import Path
from unicodedata import name

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from charindex import InvertedIndex


app = FastAPI(
    title="web moji finder", description="search for unicode characters by name"
)


class CharName(BaseModel):
    char: str
    name: str


def init(app):
    app.state.index = InvertedIndex()
    app.state.form = (Path(__file__).parent / "http_mojifinder.html").read_text()


init(app)


@app.get("/search", response_model=list[CharName])
async def search(q: str):
    chars = sorted(app.state.index.search(q))
    return ({"char": c, "name": name(c)} for c in chars)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def form():
    return app.state.form
