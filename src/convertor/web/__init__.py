import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

static_dir = Path(__file__).parent / "static"


async def convert(request):
    # request.stream()
    await asyncio.sleep(2)
    return JSONResponse({"status": "ok"})


@asynccontextmanager
async def lifespan(app):
    print(f"Ready to go. Serving static files from `{static_dir}`.")
    yield
    print("Shutdown")


routes = [
    Route("/upload", convert, methods=["PUT"]),
    Mount("/", StaticFiles(directory=static_dir, html=True)),
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
