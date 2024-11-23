import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

def detect_dominant_pitch(audio_file):
    y, sr = librosa.load(audio_file)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
    if len(pitch_values) == 0:
        return None, None
    avg_pitch = np.mean(pitch_values)
    return avg_pitch, pitch_values

def plot_pitch_over_time(pitch_values, audio_file, output_folder):
    plt.figure(figsize=(10, 4))
    plt.plot(pitch_values, label="Pitch over time")
    plt.xlabel("Frame")
    plt.ylabel("Frequency (Hz)")
    plt.title(f"Pitch Analysis: {os.path.basename(audio_file)}")
    plt.legend()
    plt.savefig(os.path.join(output_folder, f"{os.path.splitext(os.path.basename(audio_file))[0]}_pitch.png"))
    plt.close()

def create_pitch_subfolders(output_folder):
    subfolders = ['Low_Pitch', 'Medium_Pitch', 'High_Pitch']
    for subfolder in subfolders:
        subfolder_path = os.path.join(output_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

def classify_and_move_audio(audio_file, avg_pitch, output_folder):
    if avg_pitch < 300:
        category = "Low_Pitch"
    elif 300 <= avg_pitch <= 1000:
        category = "Medium_Pitch"
    else:
        category = "High_Pitch"
    category_folder = os.path.join(output_folder, category)
    shutil.copy(audio_file, os.path.join(category_folder, os.path.basename(audio_file)))

def analyze_audio_folder(folder_path):
    output_folder = os.path.join(folder_path, "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    create_pitch_subfolders(output_folder)

    result_file = os.path.join(output_folder, "pitch_analysis_results.txt")
    with open(result_file, "w") as f:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.wav', '.mp3', '.flac')):
                audio_file = os.path.join(folder_path, filename)
                print(f"Analyzing {filename}...")
                avg_pitch, pitch_values = detect_dominant_pitch(audio_file)
                if avg_pitch is None:
                    result = f"{filename}: No dominant pitch detected"
                    f.write(result + "\n")
                    print(result)
                else:
                    result = f"{filename}: Dominant pitch: {avg_pitch:.2f} Hz"
                    f.write(result + "\n")
                    print(result)
                    plot_pitch_over_time(pitch_values, audio_file, output_folder)
                    classify_and_move_audio(audio_file, avg_pitch, output_folder)
                print(f"Analysis for {filename} completed.\n")
