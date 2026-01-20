# ⚡ SIGN LANGUAGE RECOGNITION v2.0 - QUICK REFERENCE

## 🎮 KEYBOARD SHORTCUTS

| Key | Action | Mode |
|-----|--------|------|
| **'r'** | Start/Stop Recording | Both |
| **'m'** | Toggle Mode | Both |
| **'n'** | New Sign Recording | Both |
| **'q'** | Quit | Both |

---

## 📺 ON-SCREEN DISPLAY

```
MODE: RECOGNIZE (or RECORD)                              🔴
R=Record  M=Mode  N=NewSign  Q=Quit
🎥 Recording... (25/50 frames)     ← when recording
Sign: 'hello'                       ← sign name (RECORD mode)
DTW Distance: 1234.56              ← debug info

         [WEBCAM FEED HERE]

            Recognized: hello      ← result at bottom
```

---

## 🚀 QUICK START

```bash
# 1. Run the program
python main.py

# 2. In RECOGNIZE mode, press 'r' to record gesture
# 3. Perform gesture for 2 seconds
# 4. Press 'r' to stop
# 5. Hear voice output (if sign is recognized)

# To switch modes:
# Press 'm' to toggle RECORD/RECOGNIZE

# To record a new sign:
# Press 'n' → enter sign name → press 'r' to record

# To quit:
# Press 'q'
```

---

## 🎯 TYPICAL WORKFLOWS

### Recording New Signs
```
1. Press 'm' → RECORD mode
2. Press 'n' → Input sign name
3. Press 'r' → Start recording
4. Perform gesture (2 seconds)
5. Press 'r' → Stop recording
6. ✓ Sign saved
```

### Recognizing Signs
```
1. Press 'm' until "MODE: RECOGNIZE"
2. Press 'r' → Start recording
3. Perform gesture (2 seconds)
4. Press 'r' → Stop recording
5. 🔊 Hears recognized sign name
```

### Switching Modes
```
1. Press 'm' → Instant mode switch
2. No app restart needed
3. Continue immediately
```

---

## 🔧 FEATURES

✅ **Continuous Loop** - Never exits until you press 'q'  
✅ **Mode Toggle** - Switch RECORD ↔ RECOGNIZE with 'm'  
✅ **Voice Output** - Hears recognized signs (pyttsx3)  
✅ **DTW Threshold** - Filters low-confidence matches  
✅ **Live Display** - Mode, progress, distance all shown  
✅ **No Restarts** - Record multiple signs in one session  

---

## 📊 DISPLAY MEANINGS

| Text | Meaning |
|------|---------|
| Red "MODE: RECORD" | Currently in Record mode |
| Green "MODE: RECOGNIZE" | Currently in Recognize mode |
| "🎥 Recording..." | Collecting frames |
| "Sign: 'hello'" | Recording this sign name |
| "DTW Distance: X" | Match confidence (lower = better) |
| Red circle | Currently recording |
| Green/White circle | Idle/Recognized |
| "Recognized: <name>" | Best match found |

---

## 🔊 VOICE OUTPUT

**Speaks when:**
- ✅ Sign recognized with good confidence
- ✅ Different sign than before
- ✅ In RECOGNIZE mode
- ✅ Not currently recording

**Doesn't speak:**
- ❌ During recording
- ❌ "Unknown Sign" (too far from threshold)
- ❌ Same sign repeated

---

## ⚙️ DEFAULT SETTINGS

| Setting | Value | How to Change |
|---------|-------|---------------|
| DTW Threshold | 2000 | Edit sign_recorder.py |
| Voice Speed | 150 wpm | Edit utils/voice_output.py |
| Voice Volume | 0.9 | Edit utils/voice_output.py |
| Recording Frames | 50 | Edit sign_recorder.py |

---

## 🆘 TROUBLESHOOTING

**Problem: No voice output**
- Solution: Check pyttsx3 is installed: `pip install pyttsx3`

**Problem: Poor recognition**
- Solution: Record 3-5 examples per sign

**Problem: Too many "Unknown Sign"**
- Solution: Lower DTW threshold (edit sign_recorder.py)

**Problem: Too many false positives**
- Solution: Raise DTW threshold

**Problem: Webcam not opening**
- Solution: Close other apps using camera

**Problem: Program won't quit**
- Solution: Press 'q' (or Ctrl+C in terminal)

---

## 📝 EXAMPLE SESSION

```
$ python main.py
🤟 SIGN LANGUAGE RECOGNITION SYSTEM v2.0
✓ Webcam opened
✓ Starting in 'recognize' mode

[Displays: MODE: RECOGNIZE]
[User presses 'm']
✓ Switched to 'RECORD' mode

[Displays: MODE: RECORD]
[User presses 'n']
Enter sign name: hello
✓ Recording new sign: 'hello'

[User presses 'r']
🎥 Recording 'hello'...
[Displays: 🎥 Recording... (50/50 frames) and Sign: 'hello']

[After 2 seconds]
✓ Saved sign 'hello' (50 frames)

[User presses 'm']
✓ Switched to 'RECOGNIZE' mode

[Displays: MODE: RECOGNIZE]
[User presses 'r']
[Displays: 🎥 Recording... (50/50 frames)]

[After 2 seconds, automatically stops]
DTW Distances: {'hello': 850.42}
Best match: 'hello'
🔊 Voice: "hello"

[Displays: Recognized: hello]

[User presses 'q']
✓ Program closed gracefully
```

---

## 🎓 LEARNING TIPS

1. **Record clear gestures** - Consistent hand movements
2. **Good lighting** - Ensure hands are well-lit
3. **Multiple examples** - Record 3-5 per sign
4. **Same distance** - Always ~1 meter from camera
5. **Adjust threshold** - If too many unknowns/false positives

---

## 🔮 FUTURE FEATURES (TODO)

Two enhancements marked for future development:
1. **Static Alphabet** - A-Z sign recognition (separate ML model)
2. **Speech-to-Sign** - Voice input to sign translation

---

## 📞 FILES

- **main.py** - Main application loop
- **sign_recorder.py** - Recording/recognition logic
- **webcam_manager.py** - UI and display
- **utils/voice_output.py** - Text-to-speech
- **utils/sign_storage.py** - Save/load signs
- **data/signs/** - Saved sign sequences

---

## ✅ QUICK TEST

```bash
# Test: Can you do this?
python main.py
# 1. Press 'm' → See "MODE: RECORD"
# 2. Press 'n' → Enter "test"
# 3. Press 'r' → See recording progress
# 4. Wait 2 seconds, press 'r' again → See saved message
# 5. Press 'm' → See "MODE: RECOGNIZE"
# 6. Press 'r' → Wait 2 seconds, press 'r' → See result
# 7. Press 'q' → Clean exit

# If all works: ✅ System is ready!
```

---

**Status: Production Ready ✅**  
**Version: 2.0**  
**Last Updated: January 21, 2026**
