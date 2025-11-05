from flask import Flask, request, jsonify
from services.gemini_service import generate_questions, evaluate_answer
from services.pdf_service import extract_text_from_pdf
from services.tts_service import text_to_speech
from services.stt_service import speech_to_text


app = Flask(__name__)

@app.route("/ai/generate-questions", methods=["POST"])
def generate_questions_api():
    data = request.get_json()
    job = data.get("job_title")
    resume = data.get("resume_text")
    num = data.get("num", 5)
    return jsonify(generate_questions(job, resume, num))

@app.route("/ai/evaluate", methods=["POST"])
def evaluate_api():
    data = request.get_json()
    job, resume = data.get("job_title"), data.get("resume_text")
    question, answer = data.get("question"), data.get("answer")
    return jsonify(evaluate_answer(job, resume, question, answer))

@app.route("/ai/pdf-to-text", methods=["POST"])
def pdf_to_text_api():
    file = request.files["file"]
    text = extract_text_from_pdf(file)
    return jsonify({"text": text})

@app.route('/ai/tts', methods=['POST'])
def tts_api():
    data = request.get_json()
    text = data.get("text")
    voice = data.get("voice", "en-US-Standard-C")
    output_type = data.get("type", "file")  # 'file' or 'base64'
    
    return text_to_speech(text, voice, output_type)

@app.route('/ai/stt', methods=['POST'])
def stt_api():
    """Convert uploaded audio to text using Google Cloud STT."""

    # Check if 'file' is in request
    if 'file' not in request.files:
        return {"error": "No file provided. Please upload an audio file as 'file'."}, 400

    # Get uploaded file
    file = request.files['file']

    # Read bytes directly
    audio_bytes = file.read()
    if not audio_bytes:
        return {"error": "Empty audio file."}, 400

    try:
        # Pass raw bytes directly to your service function
        result = speech_to_text(audio_bytes)
        return result
    except Exception as e:
        print("STT Error:", str(e))
        return {"error": str(e)}, 500

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(port=8081, debug=True)
