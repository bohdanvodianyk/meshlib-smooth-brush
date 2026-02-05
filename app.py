from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional, Union

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from meshlib_ops import MeshlibUnavailableError, MeshOptions, process_mesh

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="MeshLib Smooth Brush")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    html_path = STATIC_DIR / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.post("/api/process")
async def process(
    file: UploadFile = File(...),
    smoothing_strength: float = Form(0.5),
    smoothing_iterations: int = Form(10),
    fill_holes: bool = Form(False),
    repair: bool = Form(False),
) -> FileResponse | JSONResponse:
    suffix = Path(file.filename or "mesh").suffix or ".stl"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        input_path = tmp_path / f"input{suffix}"
        output_path = tmp_path / f"output{suffix}"

        content = await file.read()
        input_path.write_bytes(content)

        options = MeshOptions(
            smoothing_strength=smoothing_strength,
            smoothing_iterations=smoothing_iterations,
            fill_holes=fill_holes,
            repair=repair,
        )

        try:
            process_mesh(input_path, output_path, options)
        except MeshlibUnavailableError as exc:
            return JSONResponse(
                status_code=501,
                content={
                    "error": str(exc),
                    "detail": "MeshLib is not available or the expected functions are missing.",
                },
            )

        return FileResponse(
            output_path,
            media_type="application/octet-stream",
            filename=f"processed{suffix}",
        )


@app.get("/api/health")
def health() -> dict[str, Optional[str]]:
    return {"status": "ok"}
