from flask import Flask, render_template, request, send_file, jsonify
from pytube import YouTube
import os
import moviepy.editor as mp
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        video_url = request.form['url']
        filename = download_video(video_url)
        mp3_filename = convert_to_mp3(filename)

        return send_file(mp3_filename, as_attachment=True)

    except Exception as e:
        return str(e), 500


def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.download()
    return filename

def convert_to_mp3(filename):
    mp4 = mp.AudioFileClip(filename)
    mp3 = filename.split(".mp4")[0] + ".mp3"
    mp4.write_audiofile(mp3)
    os.remove(filename)
    return mp3

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
