# Quick Start Guide

## Installation (First Time Only)

```bash
cd d:\sign_language
pip install -r requirements_updated.txt
```

## Running the Application

```bash
cd d:\sign_language
python main.py
```

Or with virtual environment:
```bash
.\.venv\Scripts\Activate.ps1
python main.py
```

---

## Workflow

### Step 1: Record Your First Sign

1. Run `python main.py`
2. Choose **1** for Record mode
3. Enter a sign name: **hello**
4. Press **r** on your keyboard to START recording
5. Perform the gesture (wave your hand) for ~2 seconds
6. Press **r** again to FINISH recording
7. ✓ Sign saved to `data/signs/hello/`

**Repeat steps 3-7 for more signs (thanks, goodbye, etc.)**

---

### Step 2: Recognize Gestures

1. Run `python main.py`
2. Choose **2** for Recognize mode (or just press Enter)
3. System loads all saved signs automatically
4. Press **r** to START recording a gesture
5. Perform a gesture matching one of your saved signs
6. Press **r** again to FINISH
7. **Result displayed**: "Recognized Sign: hello"

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **r** | Start/Stop recording |
| **q** | Quit application |

---

## Example Session

**Recording Mode:**
```
SIGN LANGUAGE RECOGNITION SYSTEM

Choose mode (1=Record, 2=Recognize, default=2): 1

SIGN RECORDING MODE

Enter sign name: hello

✓ Starting in 'RECORD' mode
Opening webcam...

Webcam ready. Press 'r' to start/finish, 'q' to quit

[Press 'r' to record]
📹 Recording 'hello'... Press 'r' again to finish
[Perform gesture]
[Press 'r' to finish]
✓ Saved sign 'hello' (50 frames) to data\signs\hello\sequence_20260121_010452.npy
```

**Recognition Mode:**
```
SIGN LANGUAGE RECOGNITION SYSTEM

Choose mode (1=Record, 2=Recognize, default=2): 2

✓ Starting in 'RECOGNIZE' mode
Opening webcam...

✓ Loaded 2 sign sequences from 1 signs
✓ SignRecorder initialized in 'recognize' mode
✓ Loaded 1 reference signs

Webcam ready. Press 'r' to start/finish, 'q' to quit

[Press 'r' to record]
📹 Recording gesture for recognition...
[Perform gesture]
[Press 'r' to finish]
DTW Distances: {'hello': 1029.9944}
✓ Best match: 'hello' (distance: 1029.9944)
Recognized Sign: hello
```

---

## Tips for Best Results

1. **Consistent Distance**: Stand 0.5-1.5 meters from the camera
2. **Good Lighting**: Ensure adequate lighting on your hands
3. **Clear Gestures**: Make deliberate, clear hand movements
4. **Record Multiple Examples**: Save 3-5 examples of each sign for better accuracy
5. **Stable Posture**: Keep your arms and body relatively still

---

## File Structure After Use

```
data/
  signs/
    hello/
      sequence_20260121_010452.npy
      sequence_20260121_010459.npy
    thanks/
      sequence_20260121_011000.npy
    goodbye/
      sequence_20260121_011015.npy
```

Each `.npy` file contains:
- Sign name
- Left hand landmarks (50 frames × 63 values)
- Right hand landmarks (50 frames × 63 values)
- Timestamp metadata

---

## Troubleshooting

**Q: "No reference signs found" message appears**
A: Record at least one sign in Record mode first

**Q: Webcam not showing**
A: Make sure no other app is using your webcam. Try closing other programs.

**Q: Poor recognition accuracy**
A: Record more examples (3-5) of each sign. Ensure consistent gestures.

**Q: Program runs slow**
A: This is normal on first use. DTW computation is CPU-intensive. It gets faster.

---

## Need Help?

- Check SYSTEM_GUIDE.md for detailed technical information
- Review the console output for debug messages
- Ensure all dependencies are installed: `pip install -r requirements_updated.txt`

---

Ready to start? Run: `python main.py`
