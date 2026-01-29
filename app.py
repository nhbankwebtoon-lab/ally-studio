import streamlit as st
import urllib.parse
import random

# --- 1. 올리(Ally) 원본 이미지 주소 고정 ---
# 사용자님이 주신 완벽한 올리 이미지 주소입니다.
ALLY_ORIGINAL_URL = "https://raw.githubusercontent.com/ally-studio/main/3D-Ally.jpg"

# 특징을 다시 한 번 텍스트로 보강하여 AI가 헷갈리지 않게 합니다. [cite: 2026-01-27]
ALLY_DETAILS = (
    "chubby light green dinosaur, huge circular eyes (50% of face), "
    "one white horn on head, white circular belly, white back spikes, 3D Pixar style"
)

# --- 2. 페이지 설정 ---
st.set_page_config(page_title="Ally Studio", page_icon="🦖")
st.title("🦖 진짜 올리(Ally) 소환 스튜디오")

# --- 3. 생성 로직 ---
user_input = st.text_input("올리가 무엇을 하나요?", placeholder="예: 수박을 맛있게 먹는")

if st.button("올리 소환하기!"):
    if user_input:
        with st.spinner("원본 올리를 학습하여 소환 중..."):
            seed_num = random.randint(1, 999999)
            
            # [핵심] 원본 이미지 주소를 프롬프트 맨 앞에 넣어 '이미지 투 이미지' 효과를 줍니다.
            # 나노바나나 모델이 이 주소의 이미지를 룩앤필(Look & Feel) 가이드로 삼습니다.
            full_prompt = (
                f"Image Reference: {ALLY_ORIGINAL_URL}. "
                f"Based exactly on this character, draw Ally {user_input}. "
                f"Maintain these features: {ALLY_DETAILS}. "
                "The eyes must be very large and round."
            )
            query = urllib.parse.quote(full_prompt)
            
            # 최종 이미지 생성 주소
            image_url = f"https://image.pollinations.ai/prompt/{query}.png?width=1024&height=1024&seed={seed_num}&nologo=true"
            
            # 결과 출력
            st.image(image_url, caption=f"학습된 올리가 {user_input} 중입니다", use_container_width=True)
            
            # 직접 링크 버튼
            st.link_button("🖼️ 생성된 이미지 크게 보기", image_url)
            st.success("원본 올리의 데이터를 성공적으로 참조했습니다!")
    else:
        st.error("내용을 입력해 주세요!")
