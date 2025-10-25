import gradio as gr
from pywhispercpp.model import Model
# import openai

# openai.api_key = "YOUR_OPENAI_API_KEY"  # replace with your key

# Simple memory for chat
chat_history = []

whisper_model = Model("/home/nik/llama-mcp/models/ggml-tiny.bin")

def transcribe_audio(audio):
    """
    Transcribe audio to text.
    Replace this with your whisper or local transcription if needed.
    """
    if audio is None:
        return ""
    
    # If using local whisper model, you can do:
    result = whisper_model.transcribe(audio)
    return result["text"]
    
    # Placeholder using OpenAI Whisper API:
    # audio_file = open(audio, "rb")
    # transcript = openai.Audio.transcriptions.create(
    #     model="whisper-1",
    #     file=audio_file
    # )

def respond(user_input):
    """
    Append user input to chat and generate AI response
    """
    chat_history.append(("user", user_input))
    # Generate response using smh
    chat_history.append(("assistant", "answer"))

    return chat_history

def voice_to_chat(audio, text_input):
    """
    Combine audio transcription and text input
    """
    transcript = transcribe_audio(audio)
    combined_input = text_input
    if transcript:
        combined_input = transcript if not text_input else f"{text_input} {transcript}"
    return respond(combined_input)

with gr.Blocks() as demo:
    gr.Markdown("## Whisper MCP demo")
    with gr.Row():
        mic_input = gr.Audio(sources=["microphone"], type="filepath")
        text_input = gr.Textbox(label="Type your message", placeholder="Type here...")
    chat_output = gr.Chatbot()
    submit_btn = gr.Button("Send")
    
    submit_btn.click(voice_to_chat, inputs=[mic_input, text_input], outputs=chat_output)

demo.launch(share=True, server_port=1233)
