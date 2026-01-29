import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO
import urllib.parse

st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 사용자님의 고정 레퍼런스 이미지 URL
ALLY_REF_URL = "https://github.com/nhbankwebtoon-lab/ally-studio/blob/main/ally_ref.png?raw=true"

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 1. 모델 설정 (404 방지를 위해 여러 이름을 시도)
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    model = None
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            break
        except:
            continue

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리가 그림을 그려서 가져오는 중..."):
                try:
                    # 2. 한글 입력을 영어로 변환 (이미지 엔진 인식용)
                    try:
                        prompt_res = model.generate_content(f"Translate '{user_input}' to English for an image prompt. Result only.")
                        english_action = prompt_res.text.strip()
                    except:
                        english_action = "swimming in the ocean" # 실패 시 기본값

                    # 3. [핵심] 이미지 주소 생성 (한글/특수문자 완벽 제거 버전)
                    # 올리의 고유 특징을 영어로 미리 고정해두었습니다.
                    base_prompt = "A cute green 3D dinosaur character with one white horn on head and very large round eyes"
                    final_prompt = f"{base_prompt}, {english_action}, high quality, 3D render style"
                    
                    # 공백을 %20 등으로 안전하게 변환
                    safe_prompt = urllib.parse.quote(final_image_prompt if 'final_image_prompt' in locals() else final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=42&nologo=true"

                    # 4. 결과 출력
                    st.success("올리가 도착했습니다!")
                    # 이미지를 먼저 띄우고 아래에 설명을 적습니다.
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")

                except Exception as e:
                    st.error(f"예상치 못한 오류가 발생했어요: {e}")
        else:
            st.warning("내용을 입력해주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해주세요.")

st.caption("© 2026 Ally Studio - Powered by Ally Engine")
