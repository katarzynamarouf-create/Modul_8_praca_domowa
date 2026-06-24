
import streamlit as st
from pydub import AudioSegment
from dotenv import load_dotenv
from openai import OpenAI
import os

def format_time(seconds):

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

load_dotenv()

client = OpenAI()

#AudioSegment.converter = r"C:\conda\envs\subtitles_app\Library\bin\ffmpeg.exe"
#AudioSegment.ffprobe = r"C:\conda\envs\subtitles_app\Library\bin\ffprobe.exe"

st.title("Generator napisów do filmów")

uploaded_file = st.file_uploader(
    "Wybierz plik wideo",
    type=["mp4", "mov", "avi"]
)

if uploaded_file:

    st.video(uploaded_file)
   
    video_path = "video.mp4"

    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Film zapisany")

    audio = AudioSegment.from_file(video_path)

    audio.export(
        "audio.mp3",
        format="mp3"
    )

    st.success("Audio wyodrębnione")

    st.audio("audio.mp3")

    if st.button("Generuj napisy"):

        with st.spinner("Generowanie napisów..."):

            with open("audio.mp3", "rb") as audio_file:

                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )
            

        edited_text = st.text_area(
            "Wygenerowane napisy",
            transcript.text,
            height=300
        )
        srt_content = ""

        for i, segment in enumerate(transcript.segments, start=1):

            srt_content += f"{i}\n"

            srt_content += (
                f"{format_time(segment.start)} --> "
                f"{format_time(segment.end)}\n"
            )

            srt_content += f"{segment.text.strip()}\n\n"


        st.download_button(
            label="Pobierz napisy",
            data=edited_text,
            file_name="napisy.txt",
            mime="text/plain"
        )
        st.download_button(
            label="Pobierz SRT",
            data=srt_content,
            file_name="napisy.srt",
            mime="text/plain"
        )