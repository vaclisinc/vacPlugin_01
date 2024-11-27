import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import ttk


# 音頻生成函數
def generate_waveform(wave_type, freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    if wave_type == "Sine":
        return np.sin(2 * np.pi * freq * t)
    elif wave_type == "Square":
        return np.sign(np.sin(2 * np.pi * freq * t))
    elif wave_type == "Sawtooth":
        return 2 * (t * freq - np.floor(0.5 + t * freq))
    elif wave_type == "Triangle":
        return 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    elif wave_type == "Noise":
        return np.random.uniform(-1, 1, len(t))
    else:
        raise ValueError("Unsupported wave type!")


# 包絡線 (ADSR)
def apply_adsr(data, sample_rate, attack, decay, sustain, release):
    total_samples = len(data)
    attack_samples = int(sample_rate * attack)
    decay_samples = int(sample_rate * decay)
    release_samples = int(sample_rate * release)
    sustain_samples = total_samples - attack_samples - decay_samples - release_samples

    envelope = np.zeros(total_samples)
    # Attack
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # Decay
    envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain, decay_samples)
    # Sustain
    envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain
    # Release
    envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)

    return data * envelope


# 播放音頻
def play_audio_with_key(note_freq):
    wave_type = waveform_combobox.get()
    duration = 0.5  # 播放時間
    sample_rate = 44100

    attack = float(attack_entry.get())
    decay = float(decay_entry.get())
    sustain = float(sustain_entry.get())
    release = float(release_entry.get())

    # 生成波形
    waveform = generate_waveform(wave_type, note_freq, duration, sample_rate)

    # 套用包絡線
    final_waveform = apply_adsr(waveform, sample_rate, attack, decay, sustain, release)

    # 正規化
    final_waveform = final_waveform / np.max(np.abs(final_waveform)) * 0.5

    # 播放音頻
    sd.play(final_waveform, samplerate=sample_rate, blocking=False)


# 停止音頻
def stop_audio():
    sd.stop()


# 建立 UI
root = tk.Tk()
root.title("假琴鍵合成器")

# 波形選擇
tk.Label(root, text="波形:").grid(row=0, column=0, padx=10, pady=5)
waveform_combobox = ttk.Combobox(root, values=["Sine", "Square", "Sawtooth", "Triangle", "Noise"])
waveform_combobox.grid(row=0, column=1, padx=10, pady=5)
waveform_combobox.set("Sine")

# ADSR 參數
tk.Label(root, text="Attack (秒):").grid(row=1, column=0, padx=10, pady=5)
attack_entry = tk.Entry(root)
attack_entry.grid(row=1, column=1, padx=10, pady=5)
attack_entry.insert(0, "0.1")

tk.Label(root, text="Decay (秒):").grid(row=2, column=0, padx=10, pady=5)
decay_entry = tk.Entry(root)
decay_entry.grid(row=2, column=1, padx=10, pady=5)
decay_entry.insert(0, "0.1")

tk.Label(root, text="Sustain (0-1):").grid(row=3, column=0, padx=10, pady=5)
sustain_entry = tk.Entry(root)
sustain_entry.grid(row=3, column=1, padx=10, pady=5)
sustain_entry.insert(0, "0.7")

tk.Label(root, text="Release (秒):").grid(row=4, column=0, padx=10, pady=5)
release_entry = tk.Entry(root)
release_entry.grid(row=4, column=1, padx=10, pady=5)
release_entry.insert(0, "0.2")

# 虛擬琴鍵
tk.Label(root, text="琴鍵:").grid(row=5, column=0, padx=10, pady=5, columnspan=2)
keyboard_frame = tk.Frame(root)
keyboard_frame.grid(row=6, column=0, columnspan=2, pady=10)

# 定義音符頻率
NOTE_FREQUENCIES = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,
    "C5": 523.25,
}

# 為每個音符創建按鈕
for i, (note, freq) in enumerate(NOTE_FREQUENCIES.items()):
    button = tk.Button(keyboard_frame, text=note, command=lambda f=freq: play_audio_with_key(f))
    button.grid(row=0, column=i, padx=5, pady=5)

# 停止按鈕
stop_button = tk.Button(root, text="停止", command=stop_audio)
stop_button.grid(row=7, column=0, columnspan=2, pady=10)

# 啟動主迴圈
root.mainloop()