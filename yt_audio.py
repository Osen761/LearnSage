import os
import subprocess

def download_and_convert_audio(video_url, output_path):
    try:
        # Ensure the output directory exists
        os.makedirs(output_path, exist_ok=True)

        mp3_file = os.path.join(output_path, 'audio.mp3')

        # Use yt-dlp to download the audio and convert it to mp3 directly
        result = subprocess.run([
            'yt-dlp', '-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3', '-o', mp3_file, video_url
        ], check=True)

        if result.returncode != 0:
            raise Exception("yt-dlp failed to download the audio.")

        print(f"Audio downloaded and converted successfully to: {mp3_file}")
        return True  # Indicate success
    except Exception as e:
        print(f"Error downloading and converting audio: {str(e)}")
        return False  # Indicate failure


if __name__ == "__main__":
    video_url = "https://youtu.be/lPvqvt55l3A?si=Y7uiQ4DwkPH6B7bw"
    output_path = "/home/osen/Music/input/"
    if download_and_convert_audio(video_url, output_path):
        input_file = os.path.join(output_path, 'audio.mp3')
        output_dir = "/home/osen/Music/output/"
    else:
        print("Skipping audio splitting due to download/conversion failure.")
