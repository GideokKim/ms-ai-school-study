
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region, ExportPlatform
from msrest.authentication import ApiKeyCredentials
import time
import uuid
import os
import dotenv
import requests
import zipfile

dotenv.load_dotenv()

training_endpoint = os.getenv("TRAINING_ENDPOINT")
prediction_endpoint = os.getenv("PREDICTION_ENDPOINT")
training_key = os.getenv("TRAINING_API_KEY")
prediction_key = os.getenv("PREDICTION_API_KEY")
prediction_resource_id = os.getenv("PREDICTION_RESOURCE_ID")

training_credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
training_client = CustomVisionTrainingClient(training_endpoint, training_credentials)

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
prediction_client = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)

project_name = "6b005-kitchen-compact"
project_description = "포크와 가위를 감지하는 모델"
domain_id = None
project_id = None

# 기존 프로젝트가 존재하는지 확인
for project in training_client.get_projects():
    if project_name == project.name:
        # 기존 프로젝트가 존재하므로 프로젝트 아이디를 가져옴
        project_id = project.id
        break

# 모든 도메인 정보를 체크하고 내가 원하는 도메인 정보와 알치할 경우, 도메인 아이디를 가져옴
for domain in training_client.get_domains():
    if domain.type == "ObjectDetection" and domain.name == "General (compact)":
        domain_id = domain.id
        break

if domain_id:
    # 프로젝트를 만들거나 프로젝트를 들고 온다.

    if project_id:
        # 이미 존재하는 경우
        print(f"프로젝트가 이미 존재합니다.")
        project = training_client.get_project(project_id)
    else:
        # 새로 만들어야 하는 경우
        print(f"새로 만들어야 하는 프로젝트입니다.")
        project = training_client.create_project(project_name, project_description, domain_id)

print(f"PROJECT\n\tID: {project.id}\n\tNAME: {project.name}\n\tDESCRIPTION: {project.description}")

exist_tag_list = training_client.get_tags(project.id)
print(f"EXIST_TAG_LIST: {exist_tag_list}")

fork_tag = None
scissors_tag = None

for tag in exist_tag_list:
    print(f"{tag.name}_tag: {tag.id} {tag.name}")
    if tag.name == "fork":
        fork_tag = tag
    elif tag.name == "scissors":
        scissors_tag = tag

if not fork_tag:
    print(f"FORK_TAG 생성")
    fork_tag = training_client.create_tag(project.id, "fork")
    training_client.create_tag(project.id, "fork")
if not scissors_tag:
    print(f"SCISSORS_TAG 생성")
    scissors_tag = training_client.create_tag(project.id, "scissors")
    training_client.create_tag(project.id, "scissors")



# [x, y, width, height]
fork_image_regions = {
    "fork_1": [ 0.145833328, 0.3509314, 0.5894608, 0.238562092 ],
    "fork_2": [ 0.294117659, 0.216944471, 0.534313738, 0.5980392 ],
    "fork_3": [ 0.09191177, 0.0682516545, 0.757352948, 0.6143791 ],
    "fork_4": [ 0.254901975, 0.185898721, 0.5232843, 0.594771266 ],
    "fork_5": [ 0.2365196, 0.128709182, 0.5845588, 0.71405226 ],
    "fork_6": [ 0.115196079, 0.133611143, 0.676470637, 0.6993464 ],
    "fork_7": [ 0.164215669, 0.31008172, 0.767156839, 0.410130739 ],
    "fork_8": [ 0.118872553, 0.318251669, 0.817401946, 0.225490168 ],
    "fork_9": [ 0.18259804, 0.2136765, 0.6335784, 0.643790841 ],
    "fork_10": [ 0.05269608, 0.282303959, 0.8088235, 0.452614367 ],
    "fork_11": [ 0.05759804, 0.0894935, 0.9007353, 0.3251634 ],
    "fork_12": [ 0.3345588, 0.07315363, 0.375, 0.9150327 ],
    "fork_13": [ 0.269607842, 0.194068655, 0.4093137, 0.6732026 ],
    "fork_14": [ 0.143382356, 0.218578458, 0.7977941, 0.295751631 ],
    "fork_15": [ 0.19240196, 0.0633497, 0.5710784, 0.8398692 ],
    "fork_16": [ 0.140931368, 0.480016381, 0.6838235, 0.240196079 ],
    "fork_17": [ 0.305147052, 0.2512582, 0.4791667, 0.5408496 ],
    "fork_18": [ 0.234068632, 0.445702642, 0.6127451, 0.344771236 ],
    "fork_19": [ 0.219362751, 0.141781077, 0.5919118, 0.6683006 ],
    "fork_20": [ 0.180147052, 0.239820287, 0.6887255, 0.235294119 ]
}
 
scissors_image_regions = {
    "scissors_1": [ 0.4007353, 0.194068655, 0.259803921, 0.6617647 ],
    "scissors_2": [ 0.426470578, 0.185898721, 0.172794119, 0.5539216 ],
    "scissors_3": [ 0.289215684, 0.259428144, 0.403186262, 0.421568632 ],
    "scissors_4": [ 0.343137264, 0.105833367, 0.332107842, 0.8055556 ],
    "scissors_5": [ 0.3125, 0.09766343, 0.435049027, 0.71405226 ],
    "scissors_6": [ 0.379901975, 0.24308826, 0.32107842, 0.5718954 ],
    "scissors_7": [ 0.341911763, 0.20714055, 0.3137255, 0.6356209 ],
    "scissors_8": [ 0.231617644, 0.08459154, 0.504901946, 0.8480392 ],
    "scissors_9": [ 0.170343131, 0.332957536, 0.767156839, 0.403594762 ],
    "scissors_10": [ 0.204656869, 0.120539248, 0.5245098, 0.743464053 ],
    "scissors_11": [ 0.05514706, 0.159754932, 0.799019635, 0.730392158 ],
    "scissors_12": [ 0.265931368, 0.169558853, 0.5061275, 0.606209159 ],
    "scissors_13": [ 0.241421565, 0.184264734, 0.448529422, 0.6830065 ],
    "scissors_14": [ 0.05759804, 0.05027781, 0.75, 0.882352948 ],
    "scissors_15": [ 0.191176474, 0.169558853, 0.6936275, 0.6748366 ],
    "scissors_16": [ 0.1004902, 0.279036, 0.6911765, 0.477124184 ],
    "scissors_17": [ 0.2720588, 0.131977156, 0.4987745, 0.6911765 ],
    "scissors_18": [ 0.180147052, 0.112369314, 0.6262255, 0.6666667 ],
    "scissors_19": [ 0.333333343, 0.0274019931, 0.443627447, 0.852941155 ],
    "scissors_20": [ 0.158088237, 0.04047389, 0.6691176, 0.843137264 ]
}

# 이미지 업로드
image_list = list()

for file_name in fork_image_regions.keys():
    with open(f"./fork/{file_name}.jpg", "rb") as image:
        left, top, width, height = fork_image_regions[file_name]
        region_list = [Region(tag_id=fork_tag.id, left=left, top=top, width=width, height=height)]
        image_data = image.read()
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_data, regions=region_list))

for file_name in scissors_image_regions.keys():
    with open(f"./scissors/{file_name}.jpg", "rb") as image:
        left, top, width, height = scissors_image_regions[file_name]
        region_list = [Region(tag_id=scissors_tag.id, left=left, top=top, width=width, height=height)]
        image_data = image.read()
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_data, regions=region_list))

upload_result = training_client.create_images_from_files(project_id=project.id, batch=ImageFileCreateBatch(images=image_list))

if upload_result.is_batch_successful:
    print("이미지 업로드 성공")
else:
    print("이미지 업로드 실패")

# 모델 훈련
exist_iteration_list = training_client.get_iterations(project.id)

if len(exist_iteration_list) > 0:
    iteration = exist_iteration_list[0]
else:
    print("ITERATION 생성")
    iteration = training_client.train_project(project.id)

while iteration.status != "Completed":
    iteration = training_client.get_iteration(project.id, iteration.id)
    print(f"iteration: {iteration.status}")
    time.sleep(5)

print("iteration 완료")

# 기존 publish된 iteration이 있는지 확인
iterations = training_client.get_iterations(project_id=project.id)
already_published = any(i.publish_name == publish_name for i in iterations if i.publish_name)

publish_name = "6b005-kitchen-compact-v1"
if already_published:
    print(f"'{publish_name}' is already published. Using existing version.")
else:
    # 새로운 iteration publish
    training_client.publish_iteration(
        project_id=project.id,
        iteration_id=iteration.id,
        publish_name=publish_name,
        prediction_id=prediction_resource_id
    )
    print(f"Successfully published iteration as '{publish_name}'")

with open("./test/test_image.jpg", "rb") as image:
    image_data = image.read()

response = prediction_client.detect_image(project_id=project.id, published_name=publish_name, image_data=image_data)

for prediction in response.predictions:
    bounding_box = prediction.bounding_box

    if prediction.probability > 0.5:
        print(f"PREDICTION: {prediction.tag_name} {prediction.probability * 100}%")
        print(f"BOUNDING_BOX: {bounding_box.left} {bounding_box.top} {bounding_box.width} {bounding_box.height}")

# 현재 iteration의 export 상태 확인
exports = training_client.get_exports(project_id=project.id, iteration_id=iteration.id)
existing_onnx_export = next((e for e in exports if e.platform == ExportPlatform.onnx), None)

if existing_onnx_export:
    print("ONNX export already exists. Using existing version.")
    export = existing_onnx_export
else:
    # 새로운 export 생성
    export = training_client.export_iteration(
        project_id=project.id,
        iteration_id=iteration.id,
        platform=ExportPlatform.onnx
    )
    print("Successfully created new ONNX export.")

exports = training_client.get_exports(project_id=project.id, iteration_id=iteration.id)
export = exports[-1]
print(export)

response = requests.get(export.download_uri)
with open("6b005-kitchen-compact-v1.zip", "wb") as f:
    f.write(response.content)

# 파일 압축 풀기
def extract_zip(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

extract_zip('6b005-kitchen-compact-v1.zip', './extracted_folder')
