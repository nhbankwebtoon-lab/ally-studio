import streamlit as st
import urllib.parse
import random

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="Ally Studio", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# --- 2. 레퍼런스 이미지 주소 설정 ---
# 중요: GitHub에서 'Raw' 버튼을 눌러 나온 주소를 넣어야 합니다.
# 만약 주소를 모르겠다면, 아래 DNA 설명을 더 상세하게 고쳐서 해결할 수 있습니다.
REFERENCE_IMAGE = "https://raw.githubusercontent.com/사용자계정/ally-studio/main/3D-Ally.jpg"

ALLY_DNA = (
    "chubby light green dinosaur, white circular belly, "
    "one white horn on head, white spikes on back, very large round eyes, "
    "3D Pixar render, vivid colors"
)

# --- 3. 사용자 입력 ---
user_input = st.text_input("올리가 무엇을 하나요?", placeholder="예: swimming")

if st.button("올리 소환하기!"):
    if user_input:
        with st.spinner("이미지를 분석하여 올리를 소환 중입니다..."):
            seed_num = random.randint(1, 1000000)
            
            # [수정 포인트] 주소 전달 오류를 막기 위해 구조를 단순화했습니다.
            # AI에게 "이 이미지를 보고(See), 이 동작을 그려라(Do)"라고 명확히 지시합니다.
            full_prompt = f"Using this character style: {REFERENCE_IMAGE}, draw Ally the dinosaur {user_input}. Details: {ALLY_DNA}"
            
            # 한글이나 특수문자 에러 방지
            encoded_query = urllib.parse.quote(full_prompt)
            
            # 최종 이미지 생성 주소
            image_url = f"https://image.pollinations.ai/prompt/{encoded_query}.png?width=1024&height=1024&seed={seed_num}"
            
            # 결과 이미지 출력
            st.image(image_url, use_container_width=True)
            st.success(f"성공! '{user_input}' 중인 올리가 소환되었습니다.")
    else:
        st.error("내용을 입력해 주세요!")
