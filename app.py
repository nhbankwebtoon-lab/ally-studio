import streamlit as st
import urllib.parse
import random

# --- 1. 올리(Ally) 정체성 절대 원칙 ---
# '큰 눈'과 '머리 위 하얀 뿔 하나'를 AI가 절대 놓치지 않게 강조했습니다.
ALLY_IDENTITY = (
    "A chubby light green dinosaur with one sharp white horn on top of its head, "
    "extremely huge circular eyes covering half of its face, a large white circular belly, "
    "white rounded spikes on its back, 3D Pixar style render, "
    "highly detailed, cute character design"
)

# --- 2. 페이지 구성 ---
st.set_page_config(page_title="Ally Studio", page_icon="🦖")
st.title("🦖 진짜 올리(Ally) 소환 스튜디오")

# --- 3. 생성 로직 ---
# 한글 표기를 '올리'로 모두 수정했습니다.
user_input = st.text_input("올리가 무엇을 하고 있나요?", placeholder="예: 수박을 맛있게 먹는")

if st.button("올리 소환하기!"):
    if user_input:
        with st.spinner(f"'{user_input}' 중인 진짜 올리를 불러오는 중..."):
            seed_num = random.randint(1, 999999)
            
            # [보강] 사용자가 입력한 행동을 맨 앞으로 배치하고, 
            # 'eating a slice of watermelon' 등의 표현이 더 강력하게 작용하도록 구성했습니다.
            full_prompt = f"Action: {user_input} while holding and eating a piece of food, Character: {ALLY_IDENTITY}"
            query = urllib.parse.quote(full_prompt)
            
            # 메인 페이지로 튕기지 않는 최신 주소 규격
            image_url = f"https://image.pollinations.ai/prompt/{query}.png?width=1024&height=1024&seed={seed_num}&nologo=true"
            
            # 결과 이미지 출력
            st.image(image_url, caption=f"결과: {user_input} 중인 올리", use_container_width=True)
            st.success(f"성공! '{user_input}' 중인 올리가 소환되었습니다.")
    else:
        st.error("내용을 입력해야 올리가 나타나요!")
