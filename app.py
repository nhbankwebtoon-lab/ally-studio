import streamlit as st
import google.generativeai as genai
import os

# --- 1. API 설정 ---
# 실제 배포 시에는 st.secrets를 사용하는 것이 안전합니다.
genai.configure(api_key="여기에_발급받은_API_키를_넣으세요")
model = genai.GenerativeModel('gemini-2.0-flash-exp') # 최신 이미지 생성 모델 설정

# --- 2. 올리(Ally) 정체성 정의 (학습 데이터 역할을 함) ---
ALLY_PROMPT_GUIDE = (
    "Character Identity: Ally is a chubby light green dinosaur. "
    "Crucial features: 1. Huge circular eyes covering half the face. "
    "2. Exactly one white horn on top of the head. "
    "3. Large white circular belly patch. 4. Small white rounded spikes on back. "
    "Style: 3D Pixar render, vibrant, high quality."
)

st.title("🦖 올리(Ally) AI 스튜디오 (Gemini API)")

user_input = st.text_input("올리가 무엇을 하고 있나요?", placeholder="예: 농장에서 당근을 뽑는")

if st.button("올리 소환하기"):
    if user_input:
        with st.spinner("Gemini AI가 올리를 정성껏 그리고 있습니다..."):
            # 유저의 입력과 올리의 정체성을 결합하여 완벽한 명령어를 만듭니다.
            final_prompt = f"{user_input}. {ALLY_PROMPT_GUIDE}"
            
            # API 호출 (이미지 생성 요청)
            # 참고: 현재 Gemini API의 이미지 생성 방식에 맞춰 호출 코드가 구성됩니다.
            response = model.generate_content(
                f"Generate a high-quality 3D image: {final_prompt}"
            )
            
            # 생성된 이미지 표시 (응답 방식에 따라 처리)
            # (실제 API 응답 구조에 맞춰 이미지를 화면에 띄웁니다.)
            st.image(response.task_result.image_url) 
            st.success("진짜 올리가 소환되었습니다!")
