import sounddevice as sd
import wavio
import time

def record_and_save(filename_template):
    """Records audio from the microphone until the user stops recording (using Ctrl+c)
    and saves it with a timestamped filename based on the provided template.

    Args:
        filename_template (str): A template string for the filename, with a
            placeholder for the timestamp (e.g., "recording_{timestamp}.wav").
    """

    # Check if sounddevice is available
    try:
        import sounddevice as sd
    except ImportError:
        print("Error: Please install the sounddevice library using 'pip install sounddevice'.")
        return

    print("Press Ctrl+c to stop recording...")
    fs = 44100  # Sample rate (adjust as needed)
    channels = 1  # Mono

    def callback(indata, frames, time, status):
        if status:
            print(status)
            return False
        return indata, []

    try:
        with sd.InputStream(samplerate=fs, channels=channels, callback=callback):
            recording = sd.rec(int(1e10), blocking=True)  # Set a very high limit
    except KeyboardInterrupt:
        print("Recording stopped.")
        frames = len(recording)
        recording = recording[:frames]  # Truncate recording based on actual captured frames

    # Get actual recording duration
    duration = len(recording) / fs

    # Generate timestamp and create filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = filename_template.format(timestamp=timestamp)

    # Save recording as WAV file
    wavio.write(filename, recording, fs, sampwidth=2)  # Adjust sampwidth if needed

    # Send recording for transcription (replace with your transcription function)
    # transcribed_text = transcribe_audio(filename)
    # print(f"Transcription: {transcribed_text}")
    print(f"Recording saved: {filename} (duration: {duration:.2f} seconds)")

if __name__ == "__main__":
    filename_template = "recording_{timestamp}.wav"
    record_and_save(filename_template)
