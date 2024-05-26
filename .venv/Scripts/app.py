import streamlit as st
import subprocess
import os
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image

# Function to call the command line program
def process_audio(input_file, beat_type, detection_method):
    output_dir = "C:\\Users\\adars\\Desktop\\kickelhack"
    os.makedirs(output_dir, exist_ok=True)
    cmd = ["C:\\Users\\adars\\PycharmProjects\\BeatVisualizer\\.venv\\Scripts\\python.exe", "C:\\Users\\adars\\PycharmProjects\\BeatVisualizer\\.venv\\Scripts\\beat_detection.py", input_file, output_dir, beat_type, detection_method]
    subprocess.run(cmd)

# Function to display audio files and allow playing
def display_audio(audio_file, index):
    audio_bytes = open(audio_file, 'rb').read()
    st.audio(audio_bytes, format='audio/wav')

# Function to display images
def display_image(image_file):
    img = Image.open(image_file)
    st.image(img, caption=image_file, use_column_width=True)

# Function to download text file
def download_text(text_file):
    with open(text_file, "r") as file:
        text = file.read()
    st.download_button(label="Download Beat Locations", data=text, file_name="beat_locations.txt", mime='text/plain')

def main():
    # st.title("Beat Detection Application")
    st.image("C:\\Users\\adars\\PycharmProjects\\BeatVisualizer\\.venv\\Scripts\\banner.svg", use_column_width=True)

    # Upload audio file
    audio_file = st.file_uploader("Upload Audio File", type=["wav"])

    beat_type = st.selectbox("Choose Beat Type", options=["Metronome", "Drum", "Meow", "Guitar", "Chicken"])
    detection_method = st.selectbox("Choose Beat Detection Method", options=["Librosa", "BeatNet"])

    if audio_file:
        # Process button
        if st.button("Process"):
            with open("input.wav", "wb") as file:
                file.write(audio_file.read())
            process_audio("input.wav", beat_type, detection_method)

            # Display outputs
            output_dir = "C:\\Users\\adars\\Desktop\\kickelhack"
            beat_locations_file = os.path.join(output_dir, "beat_locations.txt")
            waveform_image = os.path.join(output_dir, "waveform.png")
            waveform_with_beats_image = os.path.join(output_dir, "waveform_with_beats.png")
            spectrogram_image = os.path.join(output_dir, "spectrogram.png")
            spectrogram_with_beats_image = os.path.join(output_dir, "spectrogram_with_beats.png")
            # metronome_audio = os.path.join(output_dir, "metronome.wav")
            # drum_audio = os.path.join(output_dir, "drum.wav")
            beat_track_audio = os.path.join(output_dir, "beat_track.wav")
            combined_audio = os.path.join(output_dir, "combined_audio.wav")

            st.subheader("Waveform")
            display_image(waveform_image)

            st.subheader("Waveform with Beat Locations")
            display_image(waveform_with_beats_image)

            st.subheader("Spectrogram")
            display_image(spectrogram_image)

            st.subheader("Spectrogram with Beat Locations")
            display_image(spectrogram_with_beats_image)

            # if beat_type == 'Metronome':
            #     st.subheader("Metronome Audio")
            #     # display_audio(metronome_audio, 1)
            #
            # elif beat_type == 'Drum':
            #     st.subheader("Drum Audio")
            st.subheader(beat_type+" Audio")
                # display_audio(drum_audio, 2)
            display_audio(beat_track_audio, 1)

            st.subheader("Combined Audio")
            display_audio(combined_audio, 2)

            st.subheader("Beat Locations")
            download_text(beat_locations_file)

if __name__ == "__main__":
    main()
