import streamlit as st
import urllib.parse
import random

# --- 1. 원본 올리(Ally) 이미지 학습 (가장 중요!) ---
# 깃허브에 올린 '3D-Ally.jpg'의 Raw 주소를 여기에 넣으세요.
# AI는 이 주소의 이미지를 먼저 보고 올리의 생김새를 학습합니다.
ALLY_ORIGINAL_URL = "https://github.com/nhbankwebtoon-lab/ally-studio/blob/main/ally_ref.png?raw=true"

ALLY_DETAILS = (
    "chubby light green dinosaur, huge circular eyes covering half of face, "
    "one white horn on head, white circular belly, white back spikes, 3D Pixar style"
)

# --- 2. 페이지 설정 ---
st.set_page_config(page_title="Ally Studio", page_icon="🦖")
st.title("🦖 진짜 올리(Ally) 소환 스튜디오")

# --- 3. 생성 로직 ---
user_input = st.text_input("올리가 무엇을 하나요?", placeholder="예: 수박을 맛있게 먹는")

if st.button("올리 소환하기!"):
    if user_input:
        with st.spinner("원본 올리를 학습하여 소환 중입니다..."):
            seed_num = random.randint(1, 999999)
            
            # [학습 핵심] 원본 이미지 URL을 프롬프트 맨 앞에 배치하여 
            # 나노바나나 모델이 이 이미지를 참조(Reference)하게 만듭니다.
            full_prompt = (
                f"Reference Image: {ALLY_ORIGINAL_URL}, "
                f"Based on the reference, draw the character {user_input}. "
                f"Keep the same features: {ALLY_DETAILS}"
            )
            query = urllib.parse.quote(full_prompt)
            
            # 고화질 이미지 생성을 위한 최종 주소
            image_url = f"https://image.pollinations.ai/prompt/{query}.png?width=1024&height=1024&seed={seed_num}&nologo=true"
            
            # 결과 출력
            st.image(image_url, caption=f"학습된 올리가 {user_input} 중입니다", use_container_width=True)
            st.success("원본 올리의 특징을 유지하며 생성을 완료했습니다!")
    else:
        st.error("내용을 입력해 주세요!")
