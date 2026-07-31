"""Run inside Blender to audit a game-asset scene.

Example:
  blender -b asset.blend --python audit_blender_scene.py -- --json audit.json
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

import bmesh
import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=pathlib.Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--max-triangles", type=int)
    return parser.parse_args(argv)


def close(a: float, b: float = 1.0, tolerance: float = 1e-4) -> bool:
    return math.isclose(a, b, abs_tol=tolerance)


def audit():
    errors = []
    warnings = []
    objects = []
    depsgraph = bpy.context.evaluated_depsgraph_get()
    total_triangles = 0

    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    if not meshes:
        errors.append("scene contains no mesh objects")

    for obj in meshes:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            triangles = sum(
                max(0, len(poly.vertices) - 2) for poly in mesh.polygons
            )
            total_triangles += triangles
        finally:
            evaluated.to_mesh_clear()

        item_warnings = []
        item_errors = []
        scale = tuple(round(v, 6) for v in obj.scale)
        if not all(close(v) for v in obj.scale):
            item_errors.append(f"unapplied scale {scale}")
        if obj.matrix_world.to_3x3().determinant() < 0:
            item_errors.append("negative world transform determinant")

        is_collision = "collision" in obj.name.lower()
        if not obj.data.materials and not is_collision:
            item_warnings.append("no material")
        if not obj.data.uv_layers and not is_collision:
            item_warnings.append("no UV map")

        bm = bmesh.new()
        try:
            bm.from_mesh(obj.data)
            loose_vertices = sum(
                1 for vertex in bm.verts if not vertex.link_edges
            )
            non_manifold = sum(1 for edge in bm.edges if not edge.is_manifold)
            degenerate_faces = sum(
                1 for face in bm.faces if face.calc_area() <= 1e-12
            )
        finally:
            bm.free()
        if loose_vertices:
            item_errors.append(f"{loose_vertices} loose vertices")
        if degenerate_faces:
            item_errors.append(f"{degenerate_faces} zero-area faces")
        if non_manifold and not is_collision:
            item_warnings.append(f"{non_manifold} non-manifold edges")

        for material in obj.data.materials:
            if material and material.use_nodes:
                for node in material.node_tree.nodes:
                    if node.type == "TEX_IMAGE" and node.image:
                        image = node.image
                        if not image.packed_file and image.source == "FILE":
                            image_path = pathlib.Path(
                                bpy.path.abspath(image.filepath)
                            )
                            if not image_path.exists():
                                item_errors.append(
                                    f"missing texture {image.filepath}"
                                )

        for message in item_errors:
            errors.append(f"{obj.name}: {message}")
        for message in item_warnings:
            warnings.append(f"{obj.name}: {message}")
        objects.append(
            {
                "name": obj.name,
                "vertices": len(obj.data.vertices),
                "polygons": len(obj.data.polygons),
                "evaluated_triangles": triangles,
                "materials": len(obj.data.materials),
                "uv_layers": len(obj.data.uv_layers),
                "errors": item_errors,
                "warnings": item_warnings,
            }
        )

    return {
        "blend_file": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "mesh_objects": len(meshes),
        "total_triangles": total_triangles,
        "actions": [action.name for action in bpy.data.actions],
        "objects": objects,
        "errors": errors,
        "warnings": warnings,
    }


def main():
    args = parse_args()
    report = audit()
    if (
        args.max_triangles is not None
        and report["total_triangles"] > args.max_triangles
    ):
        report["errors"].append(
            f"scene has {report['total_triangles']} triangles; "
            f"budget is {args.max_triangles}"
        )
    report["ok"] = not report["errors"] and (
        not args.strict or not report["warnings"]
    )
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.json:
        args.json.write_text(output + "\n", encoding="utf-8")
    print(output)
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
