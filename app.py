# Import Flask to make the website
from flask import Flask, request, send_file, render_template

# Import requests to talk to ElevenLabs
import requests

# Set up the Flask app (think of this as the "engine" of your website)
app = Flask(__name__)

# Your ElevenLabs API key (replace with your real key)
API_KEY = 'sk_XXX'

# The URL for ElevenLabs’ text-to-speech service
API_URL = 'https://api.elevenlabs.io/v1/text-to-speech/'

# Voice ID for "Rachel" (you can change this later)
VOICE_ID = '21m00Tcm4TlvDq8ikWAM'

# Headers to tell ElevenLabs who we are and what we want
HEADERS = {
    'xi-api-key': API_KEY,
    'Content-Type': 'application/json'
}

# This is the "home page" users see when they visit your site
@app.route('/')
def home():
    # Show the HTML page we’ll make next
    return render_template('index.html')

# This runs when someone submits text to generate a voiceover
@app.route('/generate', methods=['POST'])
def generate_voiceover():
    # Get the text the user typed in the form
    user_text = request.form['text']

    # Package the text and settings to send to ElevenLabs
    data = {
        "text": user_text,
        "voice_id": VOICE_ID,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    # Send the request to ElevenLabs
    response = requests.post(API_URL + VOICE_ID, json=data, headers=HEADERS)

    # If it worked...
    if response.status_code == 200:
        # Save the audio to a file called "output.mp3"
        output_file = 'output.mp3'
        with open(output_file, 'wb') as file:
            file.write(response.content)
        # Send the file back to the user to download
        return send_file(output_file, as_attachment=True)
    else:
        # If it fails, show an error on the page
        return f"Error: {response.status_code} - {response.text}"

# Start the website when you run this file
if __name__ == "__main__":
    app.run(debug=True)