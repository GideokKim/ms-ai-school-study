import cv2
import gradio as gr

cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

def detect_faces(image):
    # 이미지 불러오기
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

with gr.Blocks() as demo:
    gr.Markdown("얼굴 검출 모델")

    with gr.Row():
        webcam_input = gr.Image(sources="webcam", streaming=True, mirror_webcam=False)
        output_image = gr.Image(streaming=True)

    def detect_face_from_webcam(image):
        return detect_faces(image)
    
    webcam_input.stream(fn=detect_face_from_webcam, inputs=webcam_input, outputs=output_image)

demo.launch(share=True)
