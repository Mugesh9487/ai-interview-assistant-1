import pyaudio
import wave
import os
import parselmouth
from parselmouth.praat import call
import numpy as np
import pandas as pd

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "data_save/recorded_audio.wav"

def record_audio(log_file="log.txt"):
    """
    Records audio from the microphone while the log file exists.
    Saves to data_save/recorded_audio.wav
    """
    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
                        
        print(f"Starting audio capture.")
        
        frames = []
        os.makedirs(os.path.dirname(WAVE_OUTPUT_FILENAME), exist_ok=True)
        
        while os.path.exists(log_file):
            # Attempt to read data, handling potential overflow
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                print(f"Audio read warning: {e}")
                
        print("Audio recording ended.")
        
    except Exception as e:
        print(f"Audio stream error: {e}")
    finally:
        # Stop and close the stream
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        p.terminate()

        # Save the recorded audio
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"Audio saved to {WAVE_OUTPUT_FILENAME}")

def extract_audio_features(wav_file=WAVE_OUTPUT_FILENAME, output_csv="data_save/audioCues.csv"):
    """
    Uses parselmouth to extract pitch, intensity, formants, and band energy.
    Saves the extracted features to audioCues.csv
    """
    if not os.path.exists(wav_file):
        print(f"ERROR: {wav_file} not found for extraction.")
        return

    try:
        sound = parselmouth.Sound(wav_file)
        
        # 1. Pitch
        pitch = sound.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        valid_pitch = pitch_values[pitch_values > 0]
        avg_pitch = np.mean(valid_pitch) if len(valid_pitch) > 0 else 0
        
        # 2. Intensity
        intensity = sound.to_intensity()
        avg_intensity = np.mean(intensity.values)
        
        # 3. Formants
        formants = sound.to_formant_burg()
        # For simplicity, getting mean F1 across valid frames
        f1_list, f2_list, f3_list = [], [], []
        for i in range(1, formants.get_number_of_frames() + 1):
            f1 = formants.get_value_at_time(1, formants.get_time_from_frame_number(i))
            if not np.isnan(f1):
                f1_list.append(f1)
                
            f2 = formants.get_value_at_time(2, formants.get_time_from_frame_number(i))
            if not np.isnan(f2):
                f2_list.append(f2)
                
            f3 = formants.get_value_at_time(3, formants.get_time_from_frame_number(i))
            if not np.isnan(f3):
                f3_list.append(f3)
                
        avg_f1 = np.mean(f1_list) if len(f1_list) > 0 else 0
        avg_f2 = np.mean(f2_list) if len(f2_list) > 0 else 0
        avg_f3 = np.mean(f3_list) if len(f3_list) > 0 else 0

        # Save to CSV
        data = {
            'AvgPitch': [avg_pitch],
            'AvgIntensity': [avg_intensity],
            'AvgF1': [avg_f1],
            'AvgF2': [avg_f2],
            'AvgF3': [avg_f3]
        }
        
        df = pd.DataFrame(data)
        df.to_csv(output_csv, index=False)
        print(f"Audio features saved to {output_csv}")
        
    except Exception as e:
        print(f"Error extracting audio features: {e}")
