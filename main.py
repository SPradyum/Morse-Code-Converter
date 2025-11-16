# morse_core.py
# Core functions: mapping, encode/decode, audio generation, utils.

import numpy as np
import wave
import io

# Standard international Morse (letters + digits + some punctuation)
SYMBOLS = {
    "a": ".-",    "b": "-...",  "c": "-.-.",  "d": "-..",   "e": ".",
    "f": "..-.",  "g": "--.",   "h": "....",  "i": "..",    "j": ".---",
    "k": "-.-",   "l": ".-..",  "m": "--",    "n": "-.",    "o": "---",
    "p": ".--.",  "q": "--.-",  "r": ".-.",   "s": "...",   "t": "-",
    "u": "..-",   "v": "...-",  "w": ".--",   "x": "-..-",  "y": "-.--",
    "z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.",
    "!": "-.-.--", "/": "-..-.",  "(": "-.--.",  ")": "-.--.-",
    "&": ".-...",  ":": "---...", ";": "-.-.-.", "=": "-...-",
    "+": ".-.-.",  "-": "-....-", "_": "..--.-", "\"": ".-..-.",
    "$": "...-..-","@": ".--.-.", " ": "/"
}

REVERSE = {v: k for k, v in SYMBOLS.items()}

def text_to_morse(text, unknown_token='[?]'):
    """Convert text -> morse string (space-separated for symbols, slash for space)"""
    text = str(text).lower()
    output = []
    for ch in text:
        if ch in SYMBOLS:
            output.append(SYMBOLS[ch])
        else:
            output.append(unknown_token)
    return " ".join(output)

def morse_to_text(morse, unknown_token='?'):
    """Convert morse (space-separated codes) -> text"""
    parts = morse.strip().split()
    out = []
    for p in parts:
        if p == "/":
            out.append(" ")
        elif p in REVERSE:
            out.append(REVERSE[p])
        else:
            out.append(unknown_token)
    return "".join(out)

# Audio generation (creates WAV bytes) using simple sine tones (dot, dash, spaces)
def morse_to_wave_bytes(morse, wpm=20, freq=700, sample_rate=44100, volume=0.5):
    """
    Generate WAV bytes for given morse string.
    Timing rules (standard):
      dot = 1 unit
      dash = 3 units
      intra-symbol gap = 1 unit (handled by silence after dot/dash)
      letter gap = 3 units
      word gap = 7 units (we represent space '/' in morse)
    wpm (words per minute) controls unit length:
      standard PARIS word: dot_duration_ms = 1200 / wpm
    """
    unit_ms = 1200.0 / float(wpm)  # milliseconds per unit
    dot_ms = unit_ms
    dash_ms = 3 * unit_ms
    intra_symbol_ms = unit_ms  # between elements of same letter
    letter_gap_ms = 3 * unit_ms
    word_gap_ms = 7 * unit_ms

    def tone(ms):
        t = np.linspace(0, ms/1000.0, int(sample_rate * ms/1000.0), False)
        signal = np.sin(2 * np.pi * freq * t) * volume
        return signal

    def silence(ms):
        n = int(sample_rate * ms/1000.0)
        return np.zeros(n)

    full = np.array([], dtype=np.float32)

    tokens = morse.strip().split(" ")
    for i, token in enumerate(tokens):
        if token == "/":
            # word gap
            full = np.concatenate((full, silence(word_gap_ms)))
            continue

        # token is sequence of dots/dashes (representing a letter)
        for j, sym in enumerate(token):
            if sym == ".":
                full = np.concatenate((full, tone(dot_ms)))
            elif sym == "-":
                full = np.concatenate((full, tone(dash_ms)))
            # intra-symbol gap after each symbol except last
            if j != len(token)-1:
                full = np.concatenate((full, silence(intra_symbol_ms)))
        # after letter, add letter gap
        if i != len(tokens)-1:
            full = np.concatenate((full, silence(letter_gap_ms)))

    # normalize to int16
    audio = np.int16(full / np.max(np.abs(full)) * 32767)

    # write to WAV bytes buffer
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes = 16 bits
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    buf.seek(0)
    return buf.read()

# Utility: save WAV file
def save_morse_wav(morse, filename, **audio_kwargs):
    data = morse_to_wave_bytes(morse, **audio_kwargs)
    with open(filename, 'wb') as f:
        f.write(data)
