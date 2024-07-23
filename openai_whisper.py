import sounddevice as sd
import soundfile as sf
import requests
from whisper import load_model

# Set the sample rate and duration for recording
sample_rate = 16000  # 16 kHz
duration = 5  # 5 seconds

# Record audio from the microphone
recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
sd.wait()

# Save the recorded audio to a WAV file
sf.write('recording.wav', recording, sample_rate)

# Read the audio file
with open('recording.wav', 'rb') as file:
    audio_data = file.read()

model = load_model("base")

results = model.transcribe(audio_data)

print(results['text'])

