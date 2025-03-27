import cv2
import gradio as gr

cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

haarcascade_files = [
    "haarcascade_frontalface_default.xml",
    "haarcascade_eye.xml",
    "haarcascade_eye_tree_eyeglasses.xml",
    "haarcascade_frontalcatface.xml",
    "haarcascade_frontalcatface_extended.xml",
    "haarcascade_frontalface_alt.xml",
    "haarcascade_frontalface_alt2.xml",
    "haarcascade_frontalface_alt_tree.xml",
    "haarcascade_fullbody.xml",
    "haarcascade_lefteye_2splits.xml",
    "haarcascade_license_plate_rus_16stages.xml",
    "haarcascade_lowerbody.xml",
    "haarcascade_profileface.xml",
    "haarcascade_righteye_2splits.xml",
    "haarcascade_russian_plate_number.xml",
    "haarcascade_smile.xml",
    "haarcascade_upperbody.xml"
]

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
        cascade_name = gr.Dropdown(label="Cascade Name", choices=haarcascade_files, value=haarcascade_files[0])
        webcam_input = gr.Image(sources="webcam", streaming=True, mirror_webcam=False)
        output_image = gr.Image(streaming=True)

    def detect_face_from_webcam(image):
        return detect_faces(image)
    
    def change_cascade(cascade_name):
        global face_cascade
        cascade_path = cv2.data.haarcascades + cascade_name
        face_cascade = cv2.CascadeClassifier(cascade_path)
    
    webcam_input.stream(fn=detect_face_from_webcam, inputs=[webcam_input], outputs=[output_image])
    cascade_name.change(fn=change_cascade, inputs=[cascade_name], outputs=[])

demo.launch(share=True)
