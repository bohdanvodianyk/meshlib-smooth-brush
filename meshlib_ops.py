from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


class MeshlibUnavailableError(RuntimeError):
    pass


@dataclass
class MeshOptions:
    smoothing_strength: float = 0.5
    smoothing_iterations: int = 10
    fill_holes: bool = False
    repair: bool = False


def _load_meshlib():
    if importlib.util.find_spec("meshlib") is None:
        return None
    import meshlib.mrmeshpy as mr  # type: ignore[import-not-found]

    return mr


def _call_first_available(module, names: Iterable[str], *args, **kwargs):
    for name in names:
        fn = getattr(module, name, None)
        if fn is not None:
            return fn(*args, **kwargs)
    raise MeshlibUnavailableError(
        "MeshLib does not expose any of the expected functions: "
        + ", ".join(names)
    )


def process_mesh(input_path: Path, output_path: Path, options: MeshOptions) -> None:
    mr = _load_meshlib()
    if mr is None:
        raise MeshlibUnavailableError(
            "MeshLib Python bindings are not installed. Install meshlib to enable processing."
        )

    mesh = _call_first_available(
        mr,
        ["loadMesh", "loadMeshFromFile", "loadMeshFile", "loadMeshFromStl"],
        str(input_path),
    )

    if options.repair:
        _call_first_available(
            mr,
            ["repairMesh", "fixMesh", "meshRepair", "repair"],
            mesh,
        )

    if options.fill_holes:
        _call_first_available(
            mr,
            ["fillHoles", "fillMeshHoles", "closeHoles"],
            mesh,
        )

    if options.smoothing_iterations > 0:
        _call_first_available(
            mr,
            ["smoothMesh", "meshSmooth", "smooth"],
            mesh,
            options.smoothing_strength,
            options.smoothing_iterations,
        )

    _call_first_available(
        mr,
        ["saveMesh", "saveMeshToFile", "saveMeshFile"],
        mesh,
        str(output_path),
    )
