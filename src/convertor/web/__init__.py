import io
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from odf.opendocument import load
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from ..convert_odf import convert_document

logger = logging.getLogger(__name__)

static_dir = Path(__file__).parent / "static"

ODT_MEDIA_TYPE = "application/vnd.oasis.opendocument.text"

config = Config(".env", env_prefix="APP_")
DEBUG = config("DEBUG", cast=bool, default=False)


def convert_bytes(content: bytes) -> bytes:
    doc = load(io.BytesIO(content))
    convert_document(doc)
    output = io.BytesIO()
    doc.save(output)
    return output.getvalue()


async def convert(request: Request):
    content = await request.body()
    try:
        result = await run_in_threadpool(convert_bytes, content)
    except Exception:
        # most likely not a valid .odt file
        logger.warning("conversion failed", exc_info=True)
        return JSONResponse({"status": "error"}, status_code=422)
    return Response(result, media_type=ODT_MEDIA_TYPE)


@asynccontextmanager
async def lifespan(app):
    print(f"Ready to go. Serving static files from `{static_dir}`.")
    yield
    print("Shutdown")


routes = [
    Route("/upload", convert, methods=["PUT"]),
    Mount("/", StaticFiles(directory=static_dir, html=True)),
]

app = Starlette(debug=DEBUG, routes=routes, lifespan=lifespan)
