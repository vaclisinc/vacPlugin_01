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
    else:
        raise ValueError("Unsupported wave type!")


# 低通濾波器
def low_pass_filter(data, cutoff, sample_rate, order=5):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return lfilter(b, a, data)


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


# 音頻播放函數
def play_audio():
    # 獲取 UI 設定的參數
    wave_type = waveform_combobox.get()
    freq = float(frequency_entry.get())
    duration = 0.2  # 即時播放一小段
    sample_rate = 44100

    attack = float(attack_entry.get())
    decay = float(decay_entry.get())
    sustain = float(sustain_entry.get())
    release = float(release_entry.get())

    # 生成波形
    waveform = generate_waveform(wave_type, freq, duration, sample_rate)

    # 套用包絡線
    final_waveform = apply_adsr(waveform, sample_rate, attack, decay, sustain, release)

    # 正規化
    final_waveform = final_waveform / np.max(np.abs(final_waveform)) * 0.5

    # 播放音頻
    sd.play(final_waveform, samplerate=sample_rate, blocking=False)


# 停止音頻
def stop_audio():
    sd.stop()


# 實時調整
def update_audio(*args):
    play_audio()


# 建立 UI
root = tk.Tk()
root.title("即時合成器")

# 波形選擇
tk.Label(root, text="波形:").grid(row=0, column=0, padx=10, pady=5)
waveform_combobox = ttk.Combobox(root, values=["Sine", "Square", "Sawtooth"])
waveform_combobox.grid(row=0, column=1, padx=10, pady=5)
waveform_combobox.set("Sine")
waveform_combobox.bind("<<ComboboxSelected>>", update_audio)

# 基頻 (Hz)
tk.Label(root, text="基頻 (Hz):").grid(row=1, column=0, padx=10, pady=5)
frequency_entry = tk.Entry(root)
frequency_entry.grid(row=1, column=1, padx=10, pady=5)
frequency_entry.insert(0, "440")
frequency_entry.bind("<KeyRelease>", update_audio)

# ADSR 參數
tk.Label(root, text="Attack (秒):").grid(row=2, column=0, padx=10, pady=5)
attack_entry = tk.Entry(root)
attack_entry.grid(row=2, column=1, padx=10, pady=5)
attack_entry.insert(0, "0.1")
attack_entry.bind("<KeyRelease>", update_audio)

tk.Label(root, text="Decay (秒):").grid(row=3, column=0, padx=10, pady=5)
decay_entry = tk.Entry(root)
decay_entry.grid(row=3, column=1, padx=10, pady=5)
decay_entry.insert(0, "0.1")
decay_entry.bind("<KeyRelease>", update_audio)

tk.Label(root, text="Sustain (0-1):").grid(row=4, column=0, padx=10, pady=5)
sustain_entry = tk.Entry(root)
sustain_entry.grid(row=4, column=1, padx=10, pady=5)
sustain_entry.insert(0, "0.7")
sustain_entry.bind("<KeyRelease>", update_audio)

tk.Label(root, text="Release (秒):").grid(row=5, column=0, padx=10, pady=5)
release_entry = tk.Entry(root)
release_entry.grid(row=5, column=1, padx=10, pady=5)
release_entry.insert(0, "0.2")
release_entry.bind("<KeyRelease>", update_audio)

# 控制按鈕
play_button = tk.Button(root, text="播放", command=play_audio)
play_button.grid(row=6, column=0, pady=10)

stop_button = tk.Button(root, text="停止", command=stop_audio)
stop_button.grid(row=6, column=1, pady=10)

# 啟動主迴圈
root.mainloop()