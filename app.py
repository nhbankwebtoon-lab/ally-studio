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
    
    # 모델 설정
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리를 실제 이미지로 그리는 중..."):
                try:
                    # 1. Gemini에게 한글 입력을 영어 이미지 프롬프트로 변환 요청
                    # (이미지 엔진은 영어를 훨씬 더 잘 이해합니다)
                    translate_prompt = f"Translate '{user_input}' to English and make it a short image prompt for a cute green dinosaur character. Output only the English prompt."
                    response = model.generate_content(translate_prompt)
                    english_prompt = response.text.strip()
                    
                    # 2. 이미지 생성용 최종 영어 프롬프트 구성
                    # 올리의 고유 특징(초록 몸, 하얀 뿔, 큰 눈)을 강제로 삽입합니다.
                    final_image_prompt = f"3D render of a cute green dinosaur named Ally with one small white horn and very large eyes, {english_prompt}, bright lighting, high quality, masterpiece"
                    
                    # 3. [중요] URL 안전 인코딩 (이미지 안 나오는 문제 해결 핵심)
                    encoded_prompt = urllib.parse.quote(final_image_prompt)
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=123&nologo=true"
                    
                    # 4. 결과 출력
                    st.success("올리가 도착했습니다!")
                    st.image(image_url, use_container_width=True)
                    st.caption(f"생성된 프롬프트: {final_image_prompt}")

                except Exception as e:
                    st.error(f"오류가 발생했어요: {e}")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
