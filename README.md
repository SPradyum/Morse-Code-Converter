# ⚡ Morse Code Converter (Python + Tkinter)

A modern, dark-themed Morse Code Converter built with **Tkinter**, **Pygame**, and **Python 3.10–3.13**.  
Convert text ↔ Morse code instantly, play Morse audio, generate WAV files, and enjoy a clean futuristic UI experience.

---

## 🚀 Features

- 🔤 **Text → Morse Conversion**
- 🔁 **Morse → Text Decoding**
- 🔊 **Audio Playback** (real-time Morse tones)
- 🎵 **WAV File Generation** (export Morse audio)
- 🎛 **Adjustable Settings**
  - WPM (words per minute)
  - Frequency (tone pitch)
- 🎨 **Futuristic Minimal Dark UI**
  - Neon cyan highlights
  - Rounded panels
  - Glow hover buttons
- ⚙️ **Clean Architecture**
  - `main.py` → all logic
  - `gui.py` → all UI
- 🖥️ **Compatible with Python 3.10 – 3.13**

---

## 📂 Project Structure

```
Text-to-Morse/
│
├── gui.py                 # Futuristic Tkinter GUI (main application window)
├── main.py                # Logic: encode, decode, audio byte generator
└── README.md
```

---

## 🧠 How It Works

### **1. Encoding**
Text is converted to Morse code using a dictionary mapping:
```
A → .-
B → -...
C → -.-.
...
```

### **2. Decoding**
Morse tokens (`.`, `-`, `/`) are mapped back to characters.

### **3. Audio Generation**
Each symbol is converted to tone durations:
- Dot `.` → 1 unit
- Dash `-` → 3 units
- Space `/` → word gap

A pure PCM WAV file is generated without external audio libraries.

---

## 🎮 Usage

### **Run the GUI**
```bash
python gui.py
```

### **1. Type text or Morse code**  
### **2. Click Encode or Decode**  
### **3. Click Play to hear Morse audio**  
### **4. Adjust WPM or Frequency**  

---

## 🔧 Requirements

Install pygame:

```bash
pip install pygame
```

Python 3.10 – 3.13 recommended.

---

## 🤝 Contributing

Pull requests are welcome!  
You can add:
- Light mode theme  
- Copy-to-clipboard  
- Morse visualizer  
- LED blinking simulation  
- Web version (Flask or React)

---

## ⭐ Support

If you find this project useful or cool, please give it a **⭐ Star on GitHub**!


