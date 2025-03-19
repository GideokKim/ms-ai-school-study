import gradio as gr
import requests
import os
import dotenv
import time
import random
from PIL import Image, ImageDraw

dotenv.load_dotenv()

AI_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AI_DOCUMENT_INTELLIGENCE_ENDPOINT")
AI_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AI_DOCUMENT_INTELLIGENCE_KEY")

def request_document_intelligence(file_path):
    endpoint = AI_DOCUMENT_INTELLIGENCE_ENDPOINT
    headers = {
        "Ocp-Apim-Subscription-key": AI_DOCUMENT_INTELLIGENCE_KEY,
        "Content-Type": "image/png"
    }

    with open(file_path, "rb") as image:
        image_data = image.read()

    response = requests.post(endpoint, headers=headers, data=image_data)
    if response.status_code == 202:
        result_url = response.headers["Operation-Location"]
        
        while True:
            result_response = requests.get(result_url, headers={ "Ocp-Apim-Subscription-key": AI_DOCUMENT_INTELLIGENCE_KEY })
            result_response_json = result_response.json()
            result_status = result_response_json["status"]
            if result_status == "running":
                print(result_status)
                time.sleep(1)
                continue
            else:
                break
        
        if result_status == "succeeded":
            print(result_status)
            return result_response_json
        else:
            return None

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_image(file_path, result_response):
    image = Image.open(file_path)
    draw = ImageDraw.Draw(image)

    blocks = result_response["analyzeResult"]["paragraphs"]
    for block in blocks:
        line_color = random_color()
        polygon_list = block["boundingRegions"][0]["polygon"]
        points = [(polygon_list[i], polygon_list[i + 1]) for i in range(0, len(polygon_list), 2)]
        draw.polygon(points, outline=line_color, width=2)
    return image

with gr.Blocks() as demo:
    def click_send(file_path):
        result_response = request_document_intelligence(file_path)
        image = draw_image(file_path, result_response)
        return image
    
    input_image = gr.Image(label="입력 이미지", type="filepath")
    send_button = gr.Button("전송")
    output_image = gr.Image(label="출력 이미지", interactive=False, type="pil")

    send_button.click(click_send, inputs=[input_image], outputs=[output_image])

demo.launch()
# request_document_intelligence("image.png")
    