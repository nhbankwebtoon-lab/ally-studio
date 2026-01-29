import streamlit as st
import urllib.parse
import random

# --- 1. 올리(Ally) 고정 외형 설정 ---
# AI가 인식하기 쉬운 핵심 단어로만 구성했습니다.
ALLY_DNA = "3D style, light green dinosaur, white circular belly, white back spikes, large round eyes, smiling"

# --- 2. 화면 구성 ---
st.set_page_config(page_title="Ally Studio", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# --- 3. 생성 로직 ---
user_input = st.text_input("올리가 무엇을 하고 있나요?", placeholder="예: 수영하는, 등산하는")

if st.button("올리 소환하기!"):
    if user_input:
        with st.spinner("메인 페이지 차단을 우회하여 올리를 불러오는 중..."):
            # 랜덤 시드로 중복 요청 방지
            seed_num = random.randint(1, 999999)
            
            # [핵심 수정] 주소 끝에 확장자(.png)를 붙이고 파라미터를 최소화하여 
            # 메인 페이지로 튕기는 현상을 원천 봉쇄합니다.
            query = f"{user_input} {ALLY_DNA}"
            encoded_query = urllib.parse.quote(query)
            
            # 가장 안정적인 다이렉트 이미지 주소 형식입니다.
            image_url = f"https://image.pollinations.ai/prompt/{encoded_query}?seed={seed_num}&width=1024&height=1024&nologo=true"
            
            # 결과 이미지 출력
            st.image(image_url, use_container_width=True)
            
            # 최후의 수단: 새 탭에서 이미지 열기 버튼
            st.link_button("🖼️ 이미지가 안 나오면 여기를 눌러 새 창에서 확인하세요", image_url)
            
            st.success(f"올리가 '{user_input}' 중인 모습을 그렸습니다!")
    else:
        st.error("내용을 입력해야 올리가 나타나요!")
