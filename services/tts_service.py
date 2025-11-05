from google.cloud import texttospeech
from flask import send_file, jsonify
import base64
import io

def text_to_speech(text, voice="en-US-Standard-C", return_type="file"):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config
    )

    # 🔍 Debug: Save to a local file
    with open("debug_output.mp3", "wb") as f:
        f.write(response.audio_content)
    print("✅ Audio saved locally as debug_output.mp3")

    if return_type == "base64":
        audio_base64 = base64.b64encode(response.audio_content).decode("utf-8")
        return {"audio_base64": audio_base64}

    else:
        audio_stream = io.BytesIO(response.audio_content)
        audio_stream.seek(0)
        return send_file(
            audio_stream,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="speech_output.mp3",
            conditional=True
        )
