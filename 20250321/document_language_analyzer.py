import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from openai import AzureOpenAI
import gradio as gr

load_dotenv()

# Document Intelligence 설정
document_endpoint = os.getenv('AI_DOCUMENT_INTELLIGENCE_ENDPOINT')
document_key = os.getenv('AI_DOCUMENT_INTELLIGENCE_KEY')
document_client = DocumentAnalysisClient(endpoint=document_endpoint, 
                                       credential=AzureKeyCredential(document_key))

# Azure OpenAI 설정
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("OPENAI_ENDPOINT")
)

def analyze_document(file_path):
    """문서를 분석하여 텍스트를 추출하는 함수"""
    with open(file_path, "rb") as f:
        poller = document_client.begin_analyze_document(
            "prebuilt-document", document=f)
        result = poller.result()

    extracted_text = " ".join([p.content for p in result.paragraphs])
    return extracted_text 

def generate_blog_post(text):
    """추출된 텍스트를 기반으로 블로그 포스팅을 생성하는 함수"""
    prompt = f"""
다음 텍스트를 기반으로 블로그 포스팅을 작성해주세요.
포스팅은 다음 형식을 따라야 합니다:
1. 제목
2. 소개
3. 주요 내용 (여러 섹션으로 구분)
4. 결론

원본 텍스트:
{text}
"""
    
    response = client.chat.completions.create(
        model="deployment-name",
        messages=[
            {"role": "system", "content": "당신은 전문적인 블로그 작성자입니다. 제목마다 적절한 이모지도 써주세요. 최대한 원본 텍스트 내용을 많이 반영해주세요."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def process_document(file_path):
    """문서 처리의 전체 파이프라인을 실행하는 함수"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
            
        # 1. 문서에서 텍스트 추출
        print("문서 분석 중...")
        extracted_text = analyze_document(file_path)
        
        if not extracted_text:
            raise ValueError("텍스트 추출에 실패했습니다.")
            
        # 2. 블로그 포스팅 생성
        print("블로그 포스팅 생성 중...")
        blog_post = generate_blog_post(extracted_text)
        
        # 3. 결과 출력
        print("\n=== 생성된 블로그 포스팅 ===")
        print(blog_post)
            
        return blog_post
        
    except FileNotFoundError as e:
        print(f"파일 오류: {str(e)}")
        return None
    except Exception as e:
        print(f"처리 중 오류 발생: {str(e)}")
        print(f"오류 유형: {type(e).__name__}")
        return None

def process_document_gradio(file):
    """Gradio 인터페이스용 문서 처리 함수"""
    try:
        if not file:
            return "파일을 선택해주세요.", "파일을 선택해주세요."
            
        extracted_text = analyze_document(file.name)
        
        if not extracted_text:
            return "텍스트 추출에 실패했습니다.", "텍스트 추출에 실패했습니다."
        
        blog_post = generate_blog_post(extracted_text)
        return blog_post, blog_post
        
    except Exception as e:
        error_message = f"오류가 발생했습니다: {str(e)}"
        return error_message, error_message

def create_gradio_interface():
    with gr.Blocks() as iface:
        gr.Markdown("""# 📝 문서 분석 및 블로그 포스트 생성기""")
        with gr.Row():
            gr.Image(value="20250321/image1.png", show_label=False, container=False, height=200)
            gr.Image(value="20250321/image2.png", show_label=False, container=False, height=200)
            gr.Image(value="20250321/image3.png", show_label=False, container=False, height=200)
            gr.Image(value="20250321/image4.png", show_label=False, container=False, height=200)
            gr.Image(value="20250321/image5.png", show_label=False, container=False, height=200)
        gr.Markdown("📄 PDF 문서를 업로드하면 자동으로 블로그 포스트를 생성합니다.")
        
        with gr.Row():
            file_input = gr.File(label="📎 문서 업로드", type="filepath")
            submit_btn = gr.Button("🚀 분석 시작", variant="primary")
        
        with gr.Row():
            output_markdown = gr.Markdown(
                label="✨ 생성된 블로그 포스트 (마크다운)",
                value=""
            )
            output_text = gr.Textbox(
                label="📋 생성된 블로그 포스트 (텍스트)",
                value="",
                lines=10,
                show_copy_button=True
            )
            
        submit_btn.click(
            fn=process_document_gradio,
            inputs=[file_input],
            outputs=[output_markdown, output_text]
        )
    
    return iface

if __name__ == "__main__":
    iface = create_gradio_interface()
    iface.launch() 