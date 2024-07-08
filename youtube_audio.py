from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import (
    OpenAIWhisperParser,
    OpenAIWhisperParserLocal,
)

# set a flag to switch between local and remote parsing
# change this to True if you want to use local parsing
local = True
# Two Karpathy lecture videos
urls = ["https://youtu.be/kCc8FmEb1nY", "https://youtu.be/VMj-3S1tku0"]

# Directory to save audio files
save_dir = "~/Downloads/YouTube"

# Transcribe the videos to text
if local:
    loader = GenericLoader(
        YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParserLocal()
    )
else:
    loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
docs = loader.load()

# Returns a list of Documents, which can be easily viewed or parsed
docs[0].page_content[0:500]