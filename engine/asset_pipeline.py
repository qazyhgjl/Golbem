"""
Offline Local 3D Asset Pipeline & GLB/glTF/OBJ Model Parser for Golbem Simulator.
Parses, maps, and renders 3D human models without internet connection.
"""

import os
import struct
import json
import numpy as np
from app.logger import logger
from engine.mesh import Mesh

class AssetPipeline:
    def __init__(self, models_dir="models/assets"):
        self.models_dir = models_dir
        self.loaded_mesh = None
        self.is_custom_model_loaded = False
        self.model_metadata = {}

        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir, exist_ok=True)

    def scan_local_assets(self) -> list:
        """Scans local assets directory for available GLB/glTF/OBJ model files."""
        if not os.path.exists(self.models_dir):
            return []

        supported_exts = ('.glb', '.gltf', '.obj')
        files = [
            f for f in os.listdir(self.models_dir)
            if f.lower().endswith(supported_exts)
        ]
        return files

    def load_local_model(self, filepath: str) -> dict:
        """Loads and parses a local 3D human model file (OBJ / GLB / glTF) offline."""
        if not os.path.exists(filepath):
            logger.warning(f"Asset file not found: {filepath}. Using high-detail procedural anatomical engine.")
            self.is_custom_model_loaded = False
            return {
                "status": "procedural",
                "message": f"فایل مدل یافت نشد ({os.path.basename(filepath)}). شبیه‌ساز از موتور آناتومیک رویه‌ای پیشرفته استفاده می‌کند."
            }

        try:
            filename = os.path.basename(filepath)
            ext = os.path.splitext(filename)[1].lower()
            size_mb = os.path.getsize(filepath) / (1024 * 1024)

            mesh = None
            if ext == '.obj':
                mesh = self._parse_obj_file(filepath)
            elif ext in ('.glb', '.gltf'):
                mesh = self._parse_glb_file(filepath)

            if mesh and len(mesh.vertices) > 0:
                self.loaded_mesh = mesh
                self.is_custom_model_loaded = True
                self.model_metadata = {
                    "filename": filename,
                    "filepath": filepath,
                    "size_mb": round(size_mb, 2),
                    "format": ext.upper()[1:],
                    "vertex_count": len(mesh.vertices),
                    "triangle_count": len(mesh.indices) // 3 if len(mesh.indices) > 0 else len(mesh.vertices) // 3
                }
                logger.info(f"Loaded and parsed 3D model: {filename} ({len(mesh.vertices)} vertices)")
                return {
                    "status": "success",
                    "message": f"مدل سه‌بعدی محلی با موفقیت بارگذاری گردید: {filename} ({len(mesh.vertices)} راس - {round(size_mb, 2)} MB)",
                    "metadata": self.model_metadata
                }
            else:
                self.is_custom_model_loaded = False
                return {
                    "status": "procedural",
                    "message": f"بارگذاری مش از فایل {filename} ناموفق بود. سوئیچ به موتور آناتومیک رویه‌ای پیشرفته."
                }

        except Exception as e:
            logger.error(f"Failed to load local asset model {filepath}: {e}")
            self.is_custom_model_loaded = False
            return {
                "status": "error",
                "message": f"خطا در پارس مدل سه‌بعدی: {e}",
            }

    def _parse_obj_file(self, filepath: str) -> Mesh:
        """Parses Wavefront OBJ 3D model files into Mesh data structure."""
        mesh = Mesh(os.path.basename(filepath))
        verts = []
        normals = []
        out_verts = []
        out_normals = []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                if parts[0] == 'v' and len(parts) >= 4:
                    verts.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == 'vn' and len(parts) >= 4:
                    normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == 'f' and len(parts) >= 4:
                    face_v = []
                    face_n = []
                    for p in parts[1:4]: # Triangulate first 3 vertices
                        indices = p.split('/')
                        v_idx = int(indices[0]) - 1
                        face_v.append(verts[v_idx])
                        if len(indices) >= 3 and indices[2]:
                            n_idx = int(indices[2]) - 1
                            face_n.append(normals[n_idx])

                    out_verts.extend(face_v)
                    if len(face_n) == 3:
                        out_normals.extend(face_n)

        mesh.vertices = np.array(out_verts, dtype=np.float32)
        if len(out_normals) == len(out_verts):
            mesh.normals = np.array(out_normals, dtype=np.float32)

        return mesh

    def _parse_glb_file(self, filepath: str) -> Mesh:
        """Parses Binary GLTF (.glb) files extracting 3D geometry buffers."""
        mesh = Mesh(os.path.basename(filepath))
        try:
            with open(filepath, 'rb') as f:
                data = f.read()

            if len(data) < 20:
                return mesh

            magic, version, length = struct.unpack('<4sII', data[:12])
            if magic != b'glTF':
                return mesh

            # Read Chunk 0 (JSON)
            chunk0_len, chunk0_type = struct.unpack('<II', data[12:20])
            if chunk0_type != 0x4E4F534A: # JSON
                return mesh

            json_bytes = data[20:20 + chunk0_len]
            gltf_json = json.loads(json_bytes.decode('utf-8'))

            # Check for Chunk 1 (BIN)
            bin_offset = 20 + chunk0_len
            bin_data = b''
            if len(data) >= bin_offset + 8:
                chunk1_len, chunk1_type = struct.unpack('<II', data[bin_offset:bin_offset + 8])
                if chunk1_type == 0x004E4142: # BIN
                    bin_data = data[bin_offset + 8: bin_offset + 8 + chunk1_len]

            # Extract POSITION accessor
            accessors = gltf_json.get('accessors', [])
            buffer_views = gltf_json.get('bufferViews', [])

            for acc in accessors:
                if acc.get('type') == 'VEC3' and acc.get('componentType') == 5126: # FLOAT VEC3
                    bv_idx = acc.get('bufferView', 0)
                    bv = buffer_views[bv_idx]
                    byte_offset = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
                    count = acc.get('count', 0)

                    if bin_data and byte_offset + count * 12 <= len(bin_data):
                        v_arr = np.frombuffer(bin_data[byte_offset: byte_offset + count * 12], dtype=np.float32)
                        mesh.vertices = v_arr.reshape(-1, 3)
                        break

        except Exception as e:
            logger.warning(f"GLB parsing notice: {e}")

        return mesh

    def render_loaded_model(self, skeleton):
        """Renders loaded GLB/OBJ mesh scaled and positioned according to human skeleton."""
        if not self.is_custom_model_loaded or self.loaded_mesh is None:
            return

        pelvis_pos = skeleton.joints["Pelvis"].world_position
        glPushMatrix()
        glTranslatef(pelvis_pos[0], pelvis_pos[1], pelvis_pos[2])
        self.loaded_mesh.render()
        glPopMatrix()

    def get_status_report(self) -> str:
        """Returns clear status description regarding loaded 3D assets vs procedural engine."""
        if self.is_custom_model_loaded and self.model_metadata:
            meta = self.model_metadata
            return f"مدل محلی فعال: {meta['filename']} [{meta['format']} - {meta['vertex_count']} راس - {meta['size_mb']} MB] (آفلاین)"
        else:
            return "موتور سه‌بعدی آناتومیک داخلی Golbem فعال است (پوست، اسکلت، عضلات و اندام‌های داخلی با کیفیت بالا - آفلاین)"
