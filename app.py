import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO
import urllib.parse

st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 사용자님의 고정 레퍼런스 이미지
ALLY_REF_URL = "https://github.com/nhbankwebtoon-lab/ally-studio/blob/main/ally_ref.png?raw=true"

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 모델 설정 (가장 안전한 버전 사용)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리의 새로운 모습을 그리는 중..."):
                try:
                    # 1. Gemini를 사용해 레퍼런스 이미지 기반의 정교한 프롬프트 생성
                    response_img = requests.get(ALLY_REF_URL)
                    ref_image = Image.open(BytesIO(response_img.content))
                    
                    analysis_prompt = [
                        f"Describe the dinosaur 'Ally' in this image. Then, write a one-sentence English image prompt for her {user_input}. "
                        "Keep her green body, white horn, and 3D style.",
                        ref_image
                    ]
                    # 모델 이름 오류(404) 방지를 위한 예외 처리
                    try:
                        analysis = model.generate_content(analysis_prompt)
                        final_prompt = analysis.text
                    except:
                        # 404가 날 경우를 대비한 기본 프롬프트
                        final_prompt = f"A cute green dinosaur with a white horn, large eyes, 3D render style, {user_input}"

                    # 2. [핵심] 외부 이미지 엔진을 사용하여 즉시 시각화
                    encoded_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
                    
                    # 3. 결과 출력
                    st.success("올리의 새로운 이미지가 완성되었습니다!")
                    st.image(image_url, caption=f"결과: {user_input}", use_container_width=True)
                    st.info("💡 텍스트 묘사: " + final_prompt[:100] + "...")

                except Exception as e:
                    st.error(f"이미지 생성 중 오류가 발생했어요: {e}")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
