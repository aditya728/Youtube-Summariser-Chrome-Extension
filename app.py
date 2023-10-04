from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from waitress import serve

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    url = request.args.get('url','')
    video_id = url.split('=')[1]
    summary = get_summary(get_transcript(video_id))
    return summary, 47

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text']for d in transcript_list])
    return transcript

def get_summary(transcript):
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

if __name__ == '__main__':   
    serve(app, host="127.0.0.1" , port=5000)
    app.run()
    