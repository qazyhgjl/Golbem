# Golbem Professional Human Anatomy & Motion Simulator

A standalone, fully offline 3D Human Anatomy & Motion Simulation software for Windows 10/11 written in Python 3.9+ with PySide6, PyOpenGL, and NumPy.

![Aesthetic Sci-Fi Medical](https://img.shields.io/badge/Aesthetic-Sci--Fi%20Medical%20Shaders-blue)
![Execution](https://img.shields.io/badge/Execution-100%25%20Offline-success)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11%20%2F%20Linux-blue)

---

## 🌟 Key Capabilities

1. **Shader-Based 3D Visual Rendering (`assets/shaders/`)**:
   - GLSL PBR-lite shaders (`medical_pbr.vert`, `medical_pbr.frag`) featuring key + fill + rim lighting, specular highlights, and Fresnel rim glow for semi-transparent skin, x-ray, and organ highlights.
   - Smooth vertex normal generation and surface shading.

2. **Real 3D Asset Loader & Mesh Pipeline (`engine/asset_pipeline.py`, `engine/mesh.py`)**:
   - Parses and renders external local `.glb`, `.gltf`, and `.obj` 3D human models placed in `models/assets/`.
   - Maps vertex geometry and positions imported models according to the 23-joint skeleton hierarchy.
   - Fallback status reporting in the status bar.

3. **Sculpted Anatomical Human Geometry & Internal Organs**:
   - Hierarchical human skeleton (Pelvis, Spine, Chest, Neck, Head, Clavicles, Arms, Hands, Fingers, Legs, Feet, Toes).
   - High-vertex 3D anatomical volume meshes for bones, ribcage, vertebral column, muscle groups, and outer skin.
   - **Internal Organs Geometry**: Anatomical 3D models for Heart (ventricles, atria, aorta), Lungs (lobed anatomical structure), Liver, Kidneys, and Stomach.
   - 7 Display Modes:
     - `Skin View` (Realistic semi-transparent cyan skin)
     - `Transparent Skin View`
     - `Skeleton View`
     - `Muscle View`
     - `X-Ray View`
     - `Internal Anatomy View` (Isolates and highlights internal organs)
     - `Joint Debug View`

4. **Pose Library & FK/IK Kinematics System**:
   - Instant pose library presets: Standing, Neutral A-Pose, T-Pose, Relaxed Standing, Looking at Camera, Sitting, Lying Down, Kneeling, Bending, Stretching.
   - Local JSON pose saving and loading (`save_pose_to_file`, `load_pose_from_file`).
   - 2-link Inverse Kinematics (IK) solver helper.

5. **Enhanced Offline Persian NLP Chat Panel**:
   - Persian text normalizer, digit converter (Persian/Arabic to English digits), and half-space handler.
   - Single & compound multi-step command interpreter (e.g. `۳۰ ثانیه بدو، بعد ۱۰ تا درازونشست بزن، بعد بایست`).
   - Supports display mode changes (`پوست را شفاف کن`, `اندام‌های داخلی را نشان بده`), anatomy item selections (`قلب را نشان بده`), and controls (`متوقف کن`, `تکرار`).

6. **Anatomy Explorer & Professional UI/UX**:
   - Tabbed sidebar featuring **Anatomy Explorer** tree hierarchy with detailed inspection descriptions for all bones, joints, muscles, and organs.
   - Viewport camera navigation: Orbit (Left Drag), Pan (Right Drag), Zoom (Scroll Wheel), Preset Views (Front, Back, Left, Right, 3/4).
   - Speed control slider (0.1x to 3.0x), Play/Pause/Stop, active motion status, and FPS counter.

---

## 🚀 Requirements & Installation

### Requirements
- Operating System: Windows 10 / Windows 11 / Linux
- Python 3.9+
- Graphics Hardware: Compatible with OpenGL 2.1+ / GLSL 1.20+ (Tested on AMD Radeon RX 580 / Intel Core i3-12100F). **No CUDA or NVIDIA dependency required.**

### Installation
```bash
pip install -r requirements.txt
```

---

## 🎮 How to Run

### Windows
Double click `run.bat` or run in terminal:
```cmd
run.bat
```

### Linux / Terminal
```bash
./run.sh
```
or
```bash
python main.py
```

---

## 💬 Example Persian Commands

- `پوست را شفاف کن`
- `اندام‌های داخلی را نشان بده`
- `قلب را نشان بده`
- `۳۰ ثانیه بدو`
- `۱۰ تا دراز و نشست بزن`
- `به مدت ۲۰ ثانیه راه برو و بعد بنشین`
- `دست چپت را بالا ببر`
- `سر را به سمت راست بچرخان`
- `۵ بار اسکوات انجام بده`
- `به حالت ایستاده برگرد`
- `تمام حرکات را متوقف کن`

---

## 🧪 Running Automated Unit Tests

Execute test suite verifying parser, skeleton kinematics, animation timing, asset pipeline, and command sequence pipeline:
```bash
python -m unittest discover -s tests
```

---

## 🔒 Privacy & Offline Commitment
This software operates 100% offline with zero cloud API dependencies, zero remote downloads, and no telemetry.
