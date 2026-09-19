# Offline AI Human Motion Simulator

A standalone, fully offline 3D Human Motion Simulation software for Windows 10/11 written in Python 3.9+ with PySide6, PyOpenGL, and NumPy.

![Sci-Fi Dark Visuals](https://img.shields.io/badge/Aesthetic-Sci--Fi%20Dark%20Cyan-blue)
![Execution](https://img.shields.io/badge/Execution-100%25%20Offline-success)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)

---

## 🌟 Key Features

1. **3D Sci-Fi Human Skeleton & Body Visualization**:
   - Hierarchical human skeleton (Pelvis, Spine, Chest, Neck, Head, Clavicles, Upper Arm, Forearm, Hand, Fingers, Upper Leg, Lower Leg, Foot, Toes).
   - Procedural 3D anatomical volume meshes for bones, muscle groups, and outer skin.
   - 6 Display Modes:
     - `Skin Mode`
     - `Transparent Skin Mode`
     - `Skeleton Mode`
     - `Muscles Mode`
     - `X-Ray Mode`
     - `Joint Debug Mode`
   - Sci-Fi cyan/blue lighting theme with orange glowing joint markers and floor grid.

2. **Offline Persian NLP Chat Panel**:
   - Persian text normalizer, digit converter (Persian/Arabic to English digits), and half-space handler.
   - Single & compound multi-step command interpreter (e.g., `۳۰ ثانیه بدو، بعد ۱۰ تا درازونشست بزن، بعد بایست`).
   - Extracts duration (`۳۰ ثانیه`), repetitions (`۱۰ تا`), action types, and controls (`متوقف کن`, `تکرار`).
   - Clear Persian status & error messaging.

3. **Animation Engine & Motion Library**:
   - Keyframed & procedural motion presets:
     - **Body States**: Idle/Standing, Look at Camera, Turn Left/Right, Walk, Run, Sit, Lie Down, Return to Standing.
     - **Exercises**: Squat, Push-up, Sit-up, Jump, Bend Forward, Stretching, Arm Raise, Arm Rotation, Leg Raise.
   - Smooth frame interpolation, duration/loop scaling, play/pause/resume/stop, and playback speed adjustment slider.

4. **Manual Joint & Skeleton Control Panel**:
   - Interactive tree selector for all 23 anatomical joints.
   - Precise XYZ rotation sliders clamped within anatomical degree-of-freedom limits.
   - Per-joint reset and full skeleton reset options.

5. **3D Interactive Viewport**:
   - Orbit (Left Mouse Drag), Pan (Right Mouse Drag), Zoom (Mouse Scroll Wheel).
   - Camera View Presets: Front (جلو), Back (پشت), Left (چپ), Right (راست), 3/4 (سه چهارم).

---

## 🚀 Requirements & Installation

### Requirements
- Operating System: Windows 10 / Windows 11 / Linux
- Python 3.9+
- Graphics Hardware: Compatible with OpenGL 2.1+ (Tested on AMD Radeon RX 580 / Intel Core i3-12100F). **No CUDA or NVIDIA dependency required.**

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

- `۳۰ ثانیه بدو`
- `۱۰ تا دراز و نشست بزن`
- `به مدت ۲۰ ثانیه راه برو و بعد بنشین`
- `دست چپت را بالا ببر`
- `سر را به سمت راست بچرخان`
- `۵ بار اسکوات انجام بده`
- `بایست و به دوربین نگاه کن`
- `تمام حرکات را متوقف کن`
- `۳۰ ثانیه بدو، بعد ۱۰ تا درازونشست بزن، بعد بایست`

---

## 🧪 Running Automated Unit Tests

Execute test suite verifying parser, skeleton kinematics, animation timing, and command sequence pipeline:
```bash
python -m unittest discover -s tests
```

---

## 📐 Extension Guide (Adding New Motions)

To add a new motion:
1. Open `animation/motion_library.py`.
2. Define keyframe pose dictionaries with joint rotations:
   ```python
   POSE_MY_MOTION = {
       "Left_UpperArm": (-90, 0, 0),
       "Right_UpperArm": (-90, 0, 0),
   }
   MOTION_PRESETS["my_motion"] = [POSE_IDLE, POSE_MY_MOTION, POSE_IDLE]
   ```
3. Add Persian vocabulary synonyms in `command/vocabulary.py`:
   ```python
   ACTION_VOCABULARY["my_motion"] = ["حرکت جدید", "انجام حرکت جدید"]
   ```

---

## 🔒 Privacy & Offline Commitment
This software operates 100% offline with zero cloud API dependencies, zero remote downloads, and no telemetry.
