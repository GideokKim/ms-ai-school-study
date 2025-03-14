import requests  # requests 라이브러리를 사용하여 HTTP 요청을 보냄  
import os
import re
import dotenv
from flask import Flask, render_template_string
import markdown

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")

# Azure OpenAI 서비스의 엔드포인트 URL  
endpoint = OPENAI_ENDPOINT
# API 키를 설정. 반드시 보안을 유지해야 하며, 실제 개발 환경에서는 환경 변수에 저장하는 것이 좋음  
api_key = OPENAI_API_KEY

# Azure AI Search 서비스의 엔드포인트 URL  
ai_search_endpoint = AZURE_SEARCH_ENDPOINT  
# Azure AI Search 서비스의 API 키  
ai_search_api_key = AZURE_SEARCH_KEY
# Azure AI Search에서 사용할 인덱스 이름  
ai_search_index = "hospital-index-lucene"
ai_search_semantic = "hospital-semantic-lucene"

def request_gpt(prompt):
    
    # HTTP 요청에 필요한 헤더 설정  
    # Content-Type은 요청 본문이 JSON 형식임을 나타냄  
    # api-key는 Azure OpenAI 서비스의 인증에 사용됨  
    headers = {  
        "Content-Type": "application/json",  
        "api-key": api_key
    }
    
    # HTTP 요청의 본문 데이터  
    # messages 리스트에는 대화의 역할(role)과 내용(content)이 포함됨  
    # "system" 역할은 모델의 행동을 정의하며, 여기서는 "남해 여행 전문가"로 설정  
    # "user" 역할은 사용자가 입력한 메시지를 나타냄  
    body = {  
        "messages": [  
            {  
                "role": "system",  # 시스템 역할: 모델의 컨텍스트 설정  
                "content": f'''너는 성남시 동물 병원을 잘 아는 전문가야.\n\n
                참조 데이터 "경기도 성남시 분당구 구미동 205-1번지 오성프라자 113호 경기도 성남시 분당구 미금로 48, 
                오성프라자 113호 (구미동) 나라 동물병원 분당구 2011-08-16 구미동 031-712-0707"라고 가정했을때 각각 "주소, 소재지도로명주소, 병원이름, 구, 개업일, 동, 전화번호"야.\n\n
                병원이름은 항상 참조 데이터 안에 ) 문자 뒤에 오는거야.
                대답할 때 병원이름은 반드시 포함해야해. 그리고 병원이름은 반드시 틀리면 안돼. 소재지도로명주소는 대답하지마.'''  # 모델에게 특정 역할을 부여  
            },  
            {  
                "role": "user",  # 사용자 역할: 사용자의 요청  
                "content": prompt  # 사용자가 알고 싶은 내용 (남해 관광지 3곳)  
            }  
        ],  
        "temperature": 0.0,  # 응답의 창의성 정도를 조절 (0.0은 보수적, 1.0은 매우 창의적)  
        "top_p": 0.95,  # 확률 분포에서 상위 p%를 선택하여 응답 생성  
        "max_tokens": 800,  # 응답에 사용할 최대 토큰 수 (토큰은 단어 및 기호 단위)  
        "data_sources": [
            {
            "type": "azure_search",
            "parameters": {
                "endpoint": ai_search_endpoint,
                "index_name": ai_search_index,
                "semantic_configuration": ai_search_semantic,
                "query_type": "semantic",
                "fields_mapping": {},
                "in_scope": True,
                "filter": None,
                "strictness": 5,
                "top_n_documents": 10,
                "authentication": {
                    "type": "api_key",
                    "key": ai_search_api_key
                },
                "key": ai_search_api_key,
                
            }
            }
        ],
    }  
    
    # POST 요청을 보내고 응답 받기  
    response = requests.post(endpoint, headers=headers, json=body)  
    print(response)

    if response.status_code == 200:

        # 응답을 JSON 형식으로 파싱  
        response_json = response.json()  
        
        # 모델이 생성한 메시지 추출  
        message = response_json['choices'][0]['message']  
        citaiton_list = message['context']['citations']

        # 역할(role)과 내용(content) 분리  
        role = message['role']  # 메시지의 역할 (예: assistant)  
        content = message['content']  # 메시지의 내용 (예: 남해 관광지 정보)   
        


        content = re.sub(r'\[doc(\d+)\]', r'[참조 \1]', content)
        return content, citaiton_list
    else:
        return "", list()
  
content, citation_list = request_gpt("구미동에 있는 동물 병원 3개 추천해줄래?")

for index in range(len(citation_list)):
    c = citation_list[index]
    print("[참조 {}]".format(index + 1))
    print(c['content'] + "\n")

app = Flask(__name__)

@app.route('/')
def index():
    prompt = "구미동에 있는 동물 병원 3개 추천해줄래?"
    content, citation_list = request_gpt(prompt)

    # Markdown을 HTML로 변환
    html_content = markdown.markdown(content)

    # HTML 콘텐츠에 사용자 친화적인 스타일 추가
    styled_html_content = f'''
    <div class="markdown-content">
        {html_content}
    </div>
    '''

    # 참조 목록 추가
    citation_html = ""
    for index, citation in enumerate(citation_list):
        citation_html += f"<div class='citation'>[참조 {index + 1}] {citation['content']}</div>"

    # HTML 템플릿 반환
    return render_template_string('''
        <html>
            <head>
                <title>Markdown Display</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f9f9f9;
                        color: #333;
                    }
                    h1 {
                        color: #4CAF50;
                        border-bottom: 2px solid #4CAF50;
                        padding-bottom: 10px;
                    }
                    h2 {
                        color: #555;
                    }
                    p {
                        margin: 10px 0;
                    }
                    .markdown-content {
                        background-color: #fff;
                        padding: 15px;
                        border-radius: 5px;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                        line-height: 1.6; /* 줄 간격 조정 */
                    }
                    .citation {
                        background-color: #e7f3fe;
                        border-left: 6px solid #2196F3;
                        margin: 10px 0;
                        padding: 10px;
                        border-radius: 4px;
                    }
                </style>
            </head>
            <body>
                <h1>응답 내용</h1>
                {{ styled_html_content|safe }}
                <h2>참조 목록</h2>
                <div>{{ citation_html|safe }}</div>
            </body>
        </html>
    ''', styled_html_content=styled_html_content, citation_html=citation_html)

if __name__ == '__main__':
    app.run(debug=True)