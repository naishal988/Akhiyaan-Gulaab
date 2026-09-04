from flask import Flask, render_template, jsonify, send_file
import os

app = Flask(__name__)

def parse_lrc(lrc_file):
    """Root folder me rakhi LRC file ko read karke JSON ready banata hai"""
    lyrics = []
    try:
        with open(lrc_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('['):
                    try:
                        time_str = line[1:9]
                        text = line[10:].strip()
                        if not text: continue
                        
                        mins = int(time_str[0:2])
                        secs = float(time_str[3:])
                        total_seconds = (mins * 60) + secs
                        
                        lyrics.append({"time": total_seconds, "text": text})
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Bhai dhyan rakhna '{lrc_file}' root folder me ho!")
    return lyrics

@app.route('/')
def index():
    # Flask automatically 'templates' folder se index.html utha lega
    return render_template('index.html')

@app.route('/api/lyrics')
def get_lyrics():
    # Lyrics API jo direct frontend ko timing degi
    lyrics_data = parse_lrc('akhiyaan.lrc')
    return jsonify(lyrics_data)

@app.route('/api/audio')
def get_audio():
    # Tumhari audio file templates folder me hai, toh hum waise hi serve karenge
    audio_path = os.path.join('templates', 'akhiyaan-gulab.mp3')
    return send_file(audio_path, mimetype='audio/mpeg')

if __name__ == '__main__':
    # Server start karne ke liye
    print("🔥 Starting the Killer Sync Player...")
    print("👉 Go to: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)