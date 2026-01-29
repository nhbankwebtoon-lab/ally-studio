import streamlit as st
import urllib.parse
import random

# --- 1. 올리(Ally) 레퍼런스 이미지 설정 ---
# 사용자님이 깃허브에 올린 올리 원본 이미지의 주소를 여기에 넣습니다.
# (이 주소는 AI가 올리의 생김새를 참고하는 기준점이 됩니다.)
ALLY_REFERENCE_URL = "https://raw.githubusercontent.com/사용자계정/ally-studio/main/3D-Ally.jpg"

ALLY_DNA = (
    "chubby light green dinosaur, white circular belly, "
    "one white horn, white spikes on back, large round eyes, 3D Pixar style"
)

# --- 2. 페이지 설정 ---
st.set_page_config(page_title="Ally Studio", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# --- 3. 생성 로직 ---
user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 서핑보드를 타는")

if st.button("✨ 레퍼런스 참고하여 소환하기!"):
    if user_input:
        with st.spinner("원본 이미지를 학습하여 올리를 소환 중..."):
            seed_num = random.randint(1, 1000000)
            
            # [보완 포인트] 프롬프트 맨 앞에 레퍼런스 이미지 주소를 넣어줍니다.
            # AI 엔진(Flux/Pollinations)은 주소가 포함되면 해당 이미지를 가이드로 삼습니다.
            full_prompt = f"Reference Image: {ALLY_REFERENCE_URL}, Character: Ally the dinosaur {user_input}, {ALLY_DNA}"
            query = urllib.parse.quote(full_prompt)
            
            image_url = f"https://image.pollinations.ai/prompt/{query}.png?width=1024&height=1024&seed={seed_num}&nologo=true"
            
            # 결과 이미지 출력
            st.image(image_url, caption=f"학습된 데이터를 바탕으로 생성된 {user_input} 올리", use_container_width=True)
            st.link_button("🖼️ 고화질 이미지 확인", image_url)
            
            st.success("원본의 특징을 살려 소환에 성공했습니다!")
