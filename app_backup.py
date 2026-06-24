import streamlit as st
from pydub import AudioSegment
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

AudioSegment.converter = r"C:\conda\envs\subtitles_app\Library\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\conda\envs\subtitles_app\Library\bin\ffprobe.exe"

st.title("Generator napisów do filmów")

uploaded_file = st.file_uploader(
    "Wybierz plik wideo",
    type=["mp4", "mov", "avi"]
)

if uploaded_file:

    st.video(uploaded_file)

    video_path = "temp/video.mp4"

    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Film zapisany")

    audio = AudioSegment.from_file(video_path)

    audio.export(
        "temp/audio.mp3",
        format="mp3"
    )

    st.success("Audio wyodrębnione")

    st.audio("temp/audio.mp3")

    if st.button("Generuj napisy"):

        with st.spinner("Generowanie napisów..."):

            with open("temp/audio.mp3", "rb") as audio_file:

                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

        edited_text = st.text_area(
            "Wygenerowane napisy",
            transcript.text,
            height=300
        )

        st.download_button(
            label="Pobierz napisy",
            data=edited_text,
            file_name="napisy.txt",
            mime="text/plain"
        )