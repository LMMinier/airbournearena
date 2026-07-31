#!/usr/bin/env python3
"""Audit a glTF 2.0 .glb or .gltf with only the Python standard library."""

from __future__ import annotations

import argparse
import json
import pathlib
import struct
from typing import Any


def load_document(path: pathlib.Path) -> dict[str, Any]:
    data = path.read_bytes()
    if path.suffix.lower() == ".gltf":
        return json.loads(data.decode("utf-8"))
    if path.suffix.lower() != ".glb":
        raise ValueError("expected .glb or .gltf")
    if len(data) < 20:
        raise ValueError("GLB is shorter than its header and JSON chunk")
    magic, version, total = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF":
        raise ValueError("invalid GLB magic")
    if version != 2:
        raise ValueError(f"unsupported GLB version {version}; expected 2")
    if total != len(data):
        raise ValueError(
            f"GLB header length {total} does not equal file length {len(data)}"
        )
    offset = 12
    document = None
    while offset + 8 <= len(data):
        chunk_length, chunk_type = struct.unpack_from("<II", data, offset)
        offset += 8
        end = offset + chunk_length
        if end > len(data):
            raise ValueError("GLB chunk extends past end of file")
        if chunk_type == 0x4E4F534A and document is None:
            document = json.loads(
                data[offset:end].rstrip(b" \t\r\n\0").decode("utf-8")
            )
        offset = end
    if document is None:
        raise ValueError("GLB has no JSON chunk")
    return document


def accessor_count(doc: dict[str, Any], index: Any) -> int | None:
    if not isinstance(index, int):
        return None
    accessors = doc.get("accessors", [])
    if not 0 <= index < len(accessors):
        return None
    count = accessors[index].get("count")
    return count if isinstance(count, int) and count >= 0 else None


def audit(
    path: pathlib.Path,
    max_bytes: int | None,
    max_triangles: int | None,
) -> dict[str, Any]:
    doc = load_document(path)
    errors: list[str] = []
    warnings: list[str] = []
    asset = doc.get("asset", {})
    if str(asset.get("version", "")) != "2.0":
        errors.append("asset.version must be 2.0")

    triangles = 0
    primitives = 0
    for mesh_i, mesh in enumerate(doc.get("meshes", [])):
        for prim_i, primitive in enumerate(mesh.get("primitives", [])):
            primitives += 1
            mode = primitive.get("mode", 4)
            position = primitive.get("attributes", {}).get("POSITION")
            position_count = accessor_count(doc, position)
            if position_count is None:
                errors.append(
                    f"mesh {mesh_i} primitive {prim_i} has no valid POSITION accessor"
                )
            index_count = accessor_count(doc, primitive.get("indices"))
            count = index_count if index_count is not None else position_count
            if mode == 4 and count is not None:
                if count % 3:
                    warnings.append(
                        f"mesh {mesh_i} primitive {prim_i} count is not divisible by 3"
                    )
                triangles += count // 3
            elif mode != 4:
                warnings.append(
                    f"mesh {mesh_i} primitive {prim_i} uses non-triangle mode {mode}"
                )

    external_uris: list[str] = []
    for group in ("buffers", "images"):
        for item in doc.get(group, []):
            uri = item.get("uri")
            if isinstance(uri, str) and not uri.startswith("data:"):
                external_uris.append(uri)
                uri_path = pathlib.PurePosixPath(uri)
                if uri_path.is_absolute() or ".." in uri_path.parts:
                    errors.append(f"unsafe external URI: {uri}")
                elif not (path.parent / uri).exists():
                    errors.append(f"missing external resource: {uri}")

    byte_size = path.stat().st_size
    if max_bytes is not None and byte_size > max_bytes:
        errors.append(f"file is {byte_size} bytes; budget is {max_bytes}")
    if max_triangles is not None and triangles > max_triangles:
        errors.append(f"asset has {triangles} triangles; budget is {max_triangles}")

    return {
        "path": str(path),
        "bytes": byte_size,
        "generator": asset.get("generator"),
        "scenes": len(doc.get("scenes", [])),
        "nodes": len(doc.get("nodes", [])),
        "meshes": len(doc.get("meshes", [])),
        "primitives": primitives,
        "triangles": triangles,
        "materials": len(doc.get("materials", [])),
        "textures": len(doc.get("textures", [])),
        "images": len(doc.get("images", [])),
        "animations": len(doc.get("animations", [])),
        "external_uris": external_uris,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset", type=pathlib.Path)
    parser.add_argument("--max-bytes", type=int)
    parser.add_argument("--max-triangles", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        report = audit(
            args.asset.resolve(),
            args.max_bytes,
            args.max_triangles,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {
            "path": str(args.asset),
            "ok": False,
            "errors": [str(exc)],
            "warnings": [],
        }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['path']}: {'PASS' if report['ok'] else 'FAIL'}")
        keys = (
            "bytes",
            "meshes",
            "primitives",
            "triangles",
            "materials",
            "textures",
            "animations",
        )
        for key in keys:
            if key in report:
                print(f"  {key}: {report[key]}")
        for warning in report.get("warnings", []):
            print(f"  warning: {warning}")
        for error in report.get("errors", []):
            print(f"  error: {error}")
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
