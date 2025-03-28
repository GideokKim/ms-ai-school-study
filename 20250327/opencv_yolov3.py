import gradio as gr
import cv2
import numpy as np
import random
import platform
from PIL import Image, ImageDraw, ImageFont
import os
import dotenv
import base64
import io
import requests
import re
import time

dotenv.load_dotenv()

OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

SPEECH_ENDPOINT = os.getenv("SPEECH_ENDPOINT")
SPEECH_API_KEY = os.getenv("SPEECH_API_KEY")

# YOLOv3 모델 파일 경로
weight_path = "yolo3/yolov3.weights"
cfg_path = "yolo3/yolov3.cfg"
names_path = "yolo3/coco_korean.names"

net = cv2.dnn.readNet(weight_path, cfg_path)

with open(names_path, "r") as f:
    label_list = f.read().strip().split("\n")

def request_gpt(image_array):
    endpoint = f"{OPENAI_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2025-01-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_API_KEY
    }

    image = Image.fromarray(image_array)

    buffered_io = io.BytesIO()
    image.save(buffered_io, format="png")
    base64_image = base64.b64encode(buffered_io.getvalue()).decode("utf-8")
    
    message_list = list()

    message_list.append({
        "role": "system",
        "content": [{
            "type": "text",
            "text": """
            너는 사진 속에서 감지된 물체를 분석하는 봇이야.
            무조건 분석 결과를 한국어로 답변해줘.        
            """
        }]
    })

    message_list.append({
        "role": "user",
        "content": [{
            "type": "text",
            "text": """
            너는 물체를 감지하는 YOLO 모델이야.
            이 사진에서 감지된 물체에 대해 감지확률과 함께 자세한 설명을 붙여줘.
            반드시 감지된 물체, 바운딩 박스 안에 있는 물체에 대해서만 설명해줘.
            부연 설명 필요없고 감지된 물체에 대해서만 설명해줘야해.
            """
        },{
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
        }]
    })

    body = {
        "messages": message_list,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 16000
    }

    response = requests.post(endpoint, headers=headers, json=body)
    print(response.status_code, response.text)
    if response.status_code == 200:
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"]
    else:
        content = response.text

    return content

def request_tts(text):
    endpoint = SPEECH_ENDPOINT
    headers = {
        "Ocp-Apim-Subscription-Key": SPEECH_API_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-32kbitrate-mono-mp3"
    }

    body = f"""
    <speak version='1.0' xml:lang='ko-KR'>
        <voice name='ko-KR-JiMinNeural'>
            <prosody rate='20%'>
                {text}
            </prosody>
        </voice>
    </speak>
    """

    response = requests.post(endpoint, headers=headers, data=body)
    print(response.status_code, response.text)

    if response.status_code == 200:
        file_name = f"tts_{time.time()}.mp3"
        with open(file_name, "wb") as f:
            f.write(response.content)
        return file_name
    else:
        return None

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_font():
    font_size = 20
    if platform.system() == "Windows":
        font = ImageFont.truetype("malgun.ttf", size=font_size)
    elif platform.system() == "Linux":
        font = ImageFont.truetype("NanumGothic.ttf", size=font_size)
    else:
        font = ImageFont.load_default(size=font_size)
    return font

def detect_objects(image):
    draw_image = Image.fromarray(image.copy())
    draw = ImageDraw.Draw(draw_image)

    height, width = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    
    layer_name_list = net.getLayerNames()
    output_layer_list = [layer_name_list[i - 1] for i in net.getUnconnectedOutLayers()]

    detection_list = net.forward(output_layer_list)

    bounding_box_list = list()
    class_id_list = list()
    confidence_list = list()

    for output in detection_list:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0:
                bounding_box = detection[:4] * np.array([width, height, width, height])
                (center_x, center_y, box_width, box_height) = bounding_box.astype("int")
                x = int(center_x - box_width / 2)
                y = int(center_y - box_height / 2)

                if x < 0:
                    x = 0
                if y < 0:
                    y = 0                    
                
                bounding_box_list.append([x, y, box_width, box_height])
                class_id_list.append(class_id)
                confidence_list.append(confidence)
    
    extracted_index_list = cv2.dnn.NMSBoxes(bounding_box_list, confidence_list, 0.5, 0.4)
    
    for extracted_index in extracted_index_list:
        x, y, w, h = bounding_box_list[extracted_index]
        confidence = confidence_list[extracted_index]
        class_id = class_id_list[extracted_index]
        label = label_list[class_id]

        color = random_color()

        draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
        draw.text((x + 5, y + 5), text=f"{label} {confidence * 100:.2f}%", fill=color, font=get_font())

    return draw_image

with gr.Blocks() as demo:

    def stream_webcam(image):
        draw_image = detect_objects(image)
        return draw_image
    
    def capture_image(image):
        return image
    
    def click_send_gpt(image_array, histories):
        content = request_gpt(image_array)

        histories.append({"role": "user", "content": gr.Image(label="감지 화면", value=image_array)})
        histories.append({"role": "assistant", "content": content})

        return histories
    
    def change_chatbot(histories):
        content = histories[-1]["content"]
        pattern = r"[^가-힣a-zA-Z\s%,\.\d]"
        cleaned_content = re.sub(pattern, "", content)
        file_name = request_tts(cleaned_content)
        return file_name
    
    with gr.Row():
        webcam_input = gr.Image(label="실시간 화면", sources="webcam", streaming=True, width=480, height=270, mirror_webcam=False)
        output_image = gr.Image(label="검출 화면", streaming=True, interactive=False)
        output_capture_image = gr.Image(label="캡쳐 화면", interactive=False)

    with gr.Row():
        capture_button = gr.Button("캡쳐")
        send_gpt_button = gr.Button("GPT 전송")

    with gr.Column():
        chatbot = gr.Chatbot(label="분석 결과", type="messages")
        chatbot_audio = gr.Audio(label="GPT 음성 결과", interactive=False, autoplay=True)

    webcam_input.stream(fn=stream_webcam, inputs=[webcam_input], outputs=[output_image])
    capture_button.click(fn=capture_image, inputs=[output_image], outputs=[output_capture_image])
    send_gpt_button.click(fn=click_send_gpt, inputs=[output_capture_image, chatbot], outputs=[chatbot])
    chatbot.change(fn=change_chatbot, inputs=[chatbot], outputs=[chatbot_audio])

demo.launch(share=True)