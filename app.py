import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # [해결 1] 404 에러 방지를 위한 모델 로드
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

    # 2. 사용자 입력창
    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리가 그림을 그려서 가져오는 중..."):
                try:
                    # [해결 2] 한글 입력을 영어 이미지 프롬프트로 변환
                    try:
                        translate_prompt = f"Translate '{user_input}' to English short phrase for an image prompt. Result only."
                        response = model.generate_content(translate_prompt)
                        eng_action = response.text.strip()
                    except:
                        eng_action = "happy and playing"

                    # [해결 3] 이미지 주소 인코딩 (엑박 방지 핵심)
                    # 올리의 고유 특징(초록 몸, 하얀 뿔, 큰 눈) 고정
                    base_ally = "A cute 3D chubby green dinosaur with one white horn and very large eyes"
                    final_prompt = f"{base_ally}, {eng_action}, high quality, bright colors"
                    
                    # URL 안전 인코딩
                    encoded_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&nologo=true"

                    # 3. 결과 출력
                    st.success("올리가 화면에 도착했습니다!")
                    st.image(image_url, use_container_width=True)
                    st.caption(f"상태: {user_input}")

                except Exception as e:
                    st.error(f"오류가 발생했습니다. 다시 시도해 주세요.")
        else:
            st.warning("무엇을 하고 있는지 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")

st.caption("© 2026 Ally Studio - Powered by Ally Engine")
