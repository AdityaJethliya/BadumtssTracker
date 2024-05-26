import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import librosa
import librosa.display
import soundfile as sf
from BeatNet.BeatNet import BeatNet

def detect_beats(input_file, detection_method):
    if detection_method == 'BeatNet':
        estimator = BeatNet(1, mode='offline', inference_model='DBN', plot=[], thread=False)
        Output = estimator.process(input_file)
        beat_times = Output[:,0]
        return beat_times

    elif detection_method == 'Librosa':
        y, sr = librosa.load(input_file)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        return beat_times

def generate_beat_track(input_file, beat_times, output_dir, beat_type):
    y, sr = librosa.load(input_file)

    # Create metronome or drum beats
    if beat_type == 'Drum':
        click_times = beat_times
        click_duration = 0.05  # Duration of each drum beat
        click = np.random.normal(size=int(sr * click_duration))
    elif beat_type == 'Metronome':
        click_times = np.repeat(beat_times, 2)
        click = np.tile([1, -1], len(beat_times))

    # Create metronome or drum track
    click_track = np.zeros_like(y)
    for i, click_start in enumerate(click_times):
        start_sample = int(sr * click_start)
        click_track[start_sample:start_sample + len(click)] += click

    # Save metronome or drum track
    filename = "beat_track.wav"
    output_path = os.path.join(output_dir, filename)
    sf.write(output_path, click_track, sr)
    return click_track


def generate_beat_track(input_file, beat_times, output_dir, beat_type):
    y, sr = librosa.load(input_file)

    if beat_type == 'Meow' or beat_type == 'Chicken' or beat_type == 'Guitar':
        meow_file = "C:\\Users\\adars\\PycharmProjects\\BeatVisualizer\\.venv\\Scripts\\" + beat_type + ".wav"
        # Load the cat meow sound
        meow, meow_sr = librosa.load(meow_file, sr=sr)
        # Resample if needed to match the input file's sample rate
        if meow_sr != sr:
            meow = librosa.resample(meow, orig_sr=meow_sr, target_sr=sr)
        click_times = beat_times
        click = meow
    elif beat_type == 'Drum':
        click_times = beat_times
        click_duration = 0.05  # Duration of each drum beat
        click = np.random.normal(size=int(sr * click_duration))
    elif beat_type == 'Metronome':
        click_times = np.repeat(beat_times, 2)
        click = np.tile([1, -1], len(beat_times))

    # Create beat track
    click_track = np.zeros_like(y)
    for click_start in click_times:
        start_sample = int(sr * click_start)
        end_sample = start_sample + len(click)
        if end_sample > len(click_track):
            break
        click_track[start_sample:end_sample] += click

    # Save beat track
    filename = "beat_track.wav"
    output_path = os.path.join(output_dir, filename)
    sf.write(output_path, click_track, sr)
    return click_track

def generate_combined_audio(input_file, beat_times, output_dir, beat_type):
    y, sr = librosa.load(input_file)

    click_track = generate_beat_track(input_file, beat_times, output_dir, beat_type)

    # Combine original audio with metronome or drum track
    combined_audio = np.vstack((y, click_track[:len(y)]))

    # Save combined audio
    output_path = os.path.join(output_dir, "combined_audio.wav")
    sf.write(output_path, combined_audio.T, sr)


def generate_csv(beat_times, output_dir):
    output_path = os.path.join(output_dir, "beat_locations.csv")
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Beat Time'])
        for beat_time in beat_times:
            writer.writerow([beat_time])

def generate_txt(beat_times, output_dir):
    output_path = os.path.join(output_dir, "beat_locations.txt")
    with open(output_path, 'w') as txtfile:
        for beat_time in beat_times:
            txtfile.write("{},Beat\n".format(beat_time))

def visualize_waveform(input_file, output_dir,max_duration=30):
    y, sr = librosa.load(input_file, duration=max_duration)
    plt.figure(figsize=(12, 6))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Waveform')
    plt.savefig(os.path.join(output_dir, 'waveform.png'))
    plt.close()


def visualize_beats(input_file, beat_times, output_dir, max_duration=30):

    y, sr = librosa.load(input_file, duration=max_duration)
    plt.figure(figsize=(12, 6))
    librosa.display.waveshow(y, sr=sr)
    plt.vlines(beat_times[beat_times <= max_duration], ymin=-1, ymax=1, color='r', linestyle='--', alpha=0.5,label='Beats')
    plt.title('Waveform with Beat Locations (up to 30 seconds)')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'waveform_with_beats.png'))
    plt.close()

def visualize_spectrogram(input_file, output_dir, max_duration=30):
    y, sr = librosa.load(input_file, duration=max_duration)
    S = librosa.stft(y)
    S_db = librosa.amplitude_to_db(abs(S))
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(output_dir, 'spectrogram.png'))
    plt.close()

def visualize_spectrogram_with_beats(input_file, beat_times, output_dir, max_duration=30):
    y, sr = librosa.load(input_file, duration=max_duration)
    S = librosa.stft(y)
    S_db = librosa.amplitude_to_db(abs(S))
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
    plt.vlines(beat_times, ymin=0, ymax=sr//2, color='r', linestyle='--', alpha=0.5, label='Beats')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram with Beat Locations')
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(output_dir, 'spectrogram_with_beats.png'))
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Beat detection command line tool')
    parser.add_argument('input_file', help='Input WAV file location')
    parser.add_argument('output_dir', help='Output directory')
    parser.add_argument('beat_type', help='Use Drum or Metronome')
    parser.add_argument('detection_method', help='Use Librosa or Beatnet')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Perform beat detection
    beat_times = detect_beats(args.input_file, args.detection_method)

    # Generate outputs
    visualize_waveform(args.input_file, args.output_dir)
    visualize_beats(args.input_file, beat_times, args.output_dir)
    visualize_spectrogram(args.input_file, args.output_dir)
    visualize_spectrogram_with_beats(args.input_file, beat_times, args.output_dir)
    generate_beat_track(args.input_file, beat_times, args.output_dir, args.beat_type)
    generate_combined_audio(args.input_file, beat_times, args.output_dir, args.beat_type)
    generate_txt(beat_times, args.output_dir)

    print("Beat detection and output generation completed.")



if __name__ == "__main__":
    main()
