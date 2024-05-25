import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import librosa
import librosa.display
import soundfile as sf
from BeatNet.BeatNet import BeatNet

def detect_beats(input_file, use_beatnet):
    if use_beatnet:
        estimator = BeatNet(1, mode='offline', inference_model='DBN', plot=[], thread=False)
        Output = estimator.process(input_file)
        beat_times = Output[:,0]
    else:
        y, sr = librosa.load(input_file)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return beat_times

def generate_metronome_track(input_file, beat_times, output_dir, use_drum=False):
    y, sr = librosa.load(input_file)

    # Create metronome or drum beats
    if use_drum:
        click_times = beat_times
        click_duration = 0.05  # Duration of each drum beat
        click = np.random.normal(size=int(sr * click_duration))
    else:
        click_times = np.repeat(beat_times, 2)
        click = np.tile([1, -1], len(beat_times))

    # Create metronome or drum track
    click_track = np.zeros_like(y)
    for i, click_start in enumerate(click_times):
        start_sample = int(sr * click_start)
        click_track[start_sample:start_sample + len(click)] += click

    # Save metronome or drum track
    output_path = os.path.join(output_dir, "metronome.wav" if not use_drum else "drum.wav")
    sf.write(output_path, click_track, sr)


def generate_combined_audio(input_file, beat_times, output_dir, use_drum=False):
    y, sr = librosa.load(input_file)

    # Create metronome or drum beats
    if use_drum:
        click_times = beat_times
        click_duration = 0.05  # Duration of each drum beat
        click = np.random.normal(size=int(sr * click_duration))
    else:
        click_times = np.repeat(beat_times, 2)
        click = np.tile([1, -1], len(beat_times))

    # Create metronome or drum track
    click_track = np.zeros_like(y)
    for i, click_start in enumerate(click_times):
        start_sample = int(sr * click_start)
        click_track[start_sample:start_sample + len(click)] += click

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
    # y, sr = librosa.load(input_file)
    # plt.figure(figsize=(12, 6))
    # librosa.display.waveshow(y, sr=sr)
    # plt.vlines(beat_times, ymin=-1, ymax=1, color='r', linestyle='--', alpha=0.5, label='Beats')
    # plt.title('Waveform with Beat Locations')
    # plt.legend()
    # plt.savefig(os.path.join(output_dir, 'waveform_with_beats.png'))
    # plt.close()

    y, sr = librosa.load(input_file, duration=max_duration)
    plt.figure(figsize=(12, 6))
    librosa.display.waveshow(y, sr=sr)
    plt.vlines(beat_times[beat_times <= max_duration], ymin=-1, ymax=1, color='r', linestyle='--', alpha=0.5,
               label='Beats')
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

    # # Load only the required portion of the audio file
    # y, sr = librosa.load(input_file, sr=None, duration=max_duration)
    #
    # # Compute the Short-Time Fourier Transform (STFT) with optimized parameters
    # hop_length = 512  # Number of samples between successive frames
    # n_fft = 2048  # Length of the FFT window
    # S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    #
    # # Convert the amplitude spectrogram to dB-scaled spectrogram
    # S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    #
    # # Plot the spectrogram with beat times
    # plt.figure(figsize=(12, 6))
    # librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', cmap='coolwarm')
    #
    # # Convert beat times to frames for vertical lines plotting
    # beat_frames = librosa.time_to_frames(beat_times, sr=sr, hop_length=hop_length)
    # plt.vlines(beat_times, ymin=0, ymax=sr / 2, color='r', linestyle='--', alpha=0.5, label='Beats')
    #
    # plt.colorbar(format='%+2.0f dB')
    # plt.title('Spectrogram with Beat Locations')
    # plt.legend(loc='upper right')
    # plt.tight_layout()
    #
    # # Save the figure
    # plt.savefig(os.path.join(output_dir, 'spectrogram_with_beats.png'))
    # plt.close()

def main():
    parser = argparse.ArgumentParser(description='Beat detection command line tool')
    parser.add_argument('input_file', help='Input WAV file location')
    parser.add_argument('output_dir', help='Output directory')
    parser.add_argument('--use_drum', action='store_true', help='Use drum sound instead of metronome')
    parser.add_argument('--use_beatnet', action='store_true', help='Use beatnet model')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Perform beat detection
    beat_times = detect_beats(args.input_file, args.use_beatnet)

    # Generate outputs
    visualize_waveform(args.input_file, args.output_dir)
    visualize_beats(args.input_file, beat_times, args.output_dir)
    visualize_spectrogram(args.input_file, args.output_dir)
    visualize_spectrogram_with_beats(args.input_file, beat_times, args.output_dir)
    generate_metronome_track(args.input_file, beat_times, args.output_dir, args.use_drum)
    generate_combined_audio(args.input_file, beat_times, args.output_dir, args.use_drum)
    generate_txt(beat_times, args.output_dir)

    print("Beat detection and output generation completed.")



if __name__ == "__main__":
    main()
