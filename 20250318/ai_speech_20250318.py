import gradio as gr
import requests
import os
import dotenv
import re
from datetime import datetime

dotenv.load_dotenv()

AI_SPEECH_STT_ENDPOINT = os.getenv("AI_SPEECH_STT_ENDPOINT")
AI_SPEECH_TTS_ENDPOINT = os.getenv("AI_SPEECH_TTS_ENDPOINT")
AI_SPEECH_KEY = os.getenv("AI_SPEECH_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")

def request_gpt(prompt):
    endpoint = OPENAI_ENDPOINT

    # method: POST

    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_API_KEY
    }

    body = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "너는 서울 맛집 블로거야. 가독성 있게 맛집은 하나만 추천하고 간결하게 작성해. 대구 사투리를 써. 문장 끝마다 이모지 3개 써"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.9,
        "top_p": 0.9,
        "max_tokens": 800
    }
    
    response = requests.post(endpoint, headers=headers, json=body)
    
    if response.status_code == 200:
        response_json = response.json()
        message = response_json["choices"][0]["message"]
        content = message["content"]
        return content
    else:
        return ""

def request_stt(file_path):
    endpoint = AI_SPEECH_STT_ENDPOINT
    headers = {
        "Content-Type": "audio/wav",
        "Ocp-Apim-Subscription-key": AI_SPEECH_KEY
    }

    with open(file_path, "rb") as audio:
        audio_data = audio.read()
    
    response = requests.post(endpoint, headers=headers, data=audio_data)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["DisplayText"]
    else:
        return ""

def request_tts(text):
    enpoint = AI_SPEECH_TTS_ENDPOINT
    
    headers = {
        "Ocp-Apim-Subscription-key": AI_SPEECH_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
        "User-Agent": "curl"
    }

    body = f"""
     <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ko-KR">
        <voice name="ko-KR-JiMinNeural">
            <prosody rate="50%">
                {text}
            </prosody>
        </voice>
    </speak>    
    """

    response = requests.post(enpoint, headers=headers, data=body)

    current_time = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
    file_name = f"tts_{current_time}.wav"
    
    if response.status_code == 200:
        with open(file_name, "wb") as audio_file:
            audio_file.write(response.content)
        return file_name
    else:
        return None

with gr.Blocks() as demo:
    def change_audio(audio_path):
        if audio_path:
            text = request_stt(audio_path)
            return text
        else:
            return ""
        
    def click_send(text):
        file_path = request_tts(text)
        if file_path:
            return file_path
        else:
            return None
        
    def click_gpt_send(prompt, histories):
        content = request_gpt(prompt=prompt)
        histories.append({"role": "user", "content": prompt})
        if content:
            histories.append({"role": "assistant", "content": content})
        else:
            histories.append({"role": "assistant", "content": "죄송합니다. 응답을 받지 못했습니다."})
        return "", histories
    
    def change_chatbot(histories):
        history = histories[-1]
        content = history["content"]
        pattern = r"^[가-힣a-zA-Z0-9\s]+$"
        emoji_pattern = r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U00002700-\U000027BF\U0001F900-\U0001F9FF\U0001F1E6-\U0001F1FF\U00002600-\U000026FF\U0001F191-\U0001F251]"

        combined_pattern = f"{pattern}|{emoji_pattern}"
        cleaned_content = re.sub(combined_pattern, "", content)

        audio_path = request_tts(cleaned_content)
        if audio_path:
            return audio_path
        else:
            return None
    
    # UI    
    gr.Markdown("# AI Speech World!! #")
    with gr.Row():
        # 좌측
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(label="🤖 나의 GPT", type="messages")
            with gr.Row():
                prompt_textbox = gr.Textbox(label="프롬프트", scale=6)
                send_gpt_button = gr.Button("전송", scale=1)

            gpt_audio = gr.Audio(interactive=False, autoplay=True)
            # prompt_textbox.submit(click_send, inputs=[prompt_textbox, chatbot], outputs=[chatbot, prompt_textbox])

        # 우측
        with gr.Column(scale=1):
            with gr.Column():
                gr.Markdown("### STT(Speech To Text) ###")
                
                input_mic = gr.Audio(label="마이크 입력", sources="microphone", type="filepath", show_download_button=True)
                output_textbox = gr.Textbox(label="텍스트", interactive=False)

            with gr.Column():
                gr.Markdown("### TTS(Text To Speech) ###")

                tts_input_textbox = gr.Textbox(label="입력", placeholder="음성 변환할 텍스트를 입력하세요.")
                send_tts_button = gr.Button("전송")
                output_tts_audio = gr.Audio(interactive=False, autoplay=True)

    # 이벤트 핸들러
    send_tts_button.click(click_send, inputs=[tts_input_textbox], outputs=[output_tts_audio])
    send_gpt_button.click(click_gpt_send, inputs=[prompt_textbox, chatbot], outputs=[prompt_textbox, chatbot])
    input_mic.change(change_audio, inputs=[input_mic], outputs=[prompt_textbox])
    chatbot.change(change_chatbot, inputs=[chatbot], outputs=[gpt_audio])

demo.launch()