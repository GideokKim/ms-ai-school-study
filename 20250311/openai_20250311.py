import requests
import os
import dotenv
import time
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")


def request_openai(prompt):
    endpoint = OPENAI_ENDPOINT

    # method: POST

    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_API_KEY
    }

    body = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    
    while True:
        response = requests.post(endpoint, headers=headers, json=body)
        response_json = response.json()
        if response.status_code == 429:
            print(response_json["error"]["message"])
            time.sleep(5)
            continue
        elif response.status_code == 200:
            image_url = response_json["data"][0]["url"]
            return image_url
        else:
            print(response.json())
            time.sleep(5)
            continue


def show_image(image_url):
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))

    root = tk.Tk()
    root.title("Generated Image")

    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=img_tk)
    label.pack()

    root.mainloop()


if __name__ == "__main__":
    prompt = "꽁꽁 얼어붙은 한강 위로 고양이가 걸어다닙니다"
    image_url = request_openai(prompt)
    show_image(image_url)
