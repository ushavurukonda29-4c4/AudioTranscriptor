# ==========================================================
# GEMINI AUDIO TRANSCRIPTION (SAFE VERSION)
# ==========================================================

import os
import gradio as gr
from google import genai

# ==========================================================
# LOAD API KEY FROM ENV
# ==========================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("⚠️ GEMINI_API_KEY not found. Set it before running.")

client = genai.Client(api_key=API_KEY)

# ==========================================================
# TRANSCRIBE FUNCTION
# ==========================================================

def transcribe(audio_path):

    # Validation
    if not audio_path:
        return "❌ Please record or upload audio."

    if not API_KEY:
        return "❌ API key missing. Set GEMINI_API_KEY."

    try:
        # Upload file to Gemini
        audio_file = client.files.upload(file=audio_path)

        # Ask model to transcribe
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Transcribe this audio exactly as spoken. Do not summarize. Include punctuation.",
                audio_file
            ],
        )

        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ==========================================================
# UI (GRADIO)
# ==========================================================

with gr.Blocks(title="Gemini Audio Transcription") as demo:

    gr.Markdown("# 🎤 Audio Transcription (Gemini)")
    gr.Markdown("Record your voice and convert it to text")

    audio_input = gr.Audio(
        sources=["microphone", "upload"],
        type="filepath",
        label="🎙️ Record or Upload Audio"
    )

    output_text = gr.Textbox(
        label="📝 Transcript",
        lines=10,
        placeholder="Transcription will appear here..."
    )

    transcribe_btn = gr.Button("🚀 Transcribe")

    transcribe_btn.click(
        fn=transcribe,
        inputs=[audio_input],
        outputs=[output_text]
    )

# ==========================================================
# LAUNCH (DEPLOYMENT READY)
# ==========================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
