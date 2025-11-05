from google.cloud import speech

def speech_to_text(audio_bytes):
    """Convert raw audio (16kHz WAV) to text using Google Speech-to-Text."""
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    transcript = " ".join(r.alternatives[0].transcript for r in response.results)
    return {"transcript": transcript}
