import requests
import os
import dotenv
import markdown

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")

def display_markdown(content):
    # Markdown을 HTML로 변환
    html_content = markdown.markdown(content)
    print(html_content)  # HTML로 변환된 내용을 출력

def request_openai(prompt):
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
      "content": "너는 남해 여행 전문가야."
    },
    {
      "role": "user",
      "content": prompt
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800
}
    
    response = requests.post(endpoint, headers=headers, json=body)
    response_json = response.json()

    message = response_json["choices"][0]["message"]
    content_filter = response_json["choices"][0]["content_filter_results"]
    role = message["role"]
    content = message["content"]
    display_markdown(content)
    return role, content, content_filter

if __name__ == "__main__":
    prompt = "남해 연인 데이트 장소 추천해줘"
    role, content, content_filter = request_openai(prompt)
    # print(role)
    # print(content)
    # print(content_filter)
