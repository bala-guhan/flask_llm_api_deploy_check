import os
from flask import Flask, render_template, request
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import re
from dotenv import load_dotenv  
import time

app = Flask(__name__)

load_dotenv() 

GENAI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GENAI_API_KEY)
@app.route('/', methods=['GET', 'POST'])
def home():
    response = None
    video_id = None
    error_message = None
    
    if request.method == 'POST':
        url = request.form['query']
        
        def get_video_id(url):
            pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
            match = re.search(pattern, url)
            if match:
                return match.group(1)
            raise ValueError("Invalid YouTube URL")

        def fetch_transcript(video_id, retries=3):
            for attempt in range(retries):
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    return transcript
                except NoTranscriptFound:
                    return "No subtitles available for this video."

        def summarize_text(content):
            prompt_template = (
                "Summarize the following text from a YouTube video transcript:\n\n"
                f"{content}\n\n"
                "Summary:"
            )
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt_template).text
            return response

        try:
            video_id = get_video_id(url)  # Extract video ID
            # Fetch transcript using the video ID
            transcript = fetch_transcript(video_id)
            if transcript:
                summary = summarize_text(transcript)  # Generate summary
            else:
                summary = "Transcript not available for this video."
            response = summary
        except ValueError as ve:
            error_message = f"Error: {ve}"
        except Exception as e:
            error_message = f"An error occurred: {e}"
    
    return render_template('query_form.html', response=response, video_id=video_id, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
