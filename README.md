# MeshLib Smooth Brush

A lightweight web app for smoothing STL/PLY meshes with MeshLib. The UI provides
options for smoothing strength/iterations, hole filling, and mesh repair.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Mesh processing requires MeshLib Python bindings:

```bash
pip install meshlib
```

## Run

```bash
uvicorn app:app --reload
```

Then open http://localhost:8000.

## Notes

The MeshLib Python API may expose different function names depending on the
version. If you encounter errors about missing functions, update the function
lists in `meshlib_ops.py` to match the MeshLib API in your environment.
