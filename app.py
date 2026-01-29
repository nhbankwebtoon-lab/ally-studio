import streamlit as st
import urllib.parse
import random

# --- 1. 올리(Ally) 정체성 강화 --- [cite: 2026-01-27]
# 특징: 연두색 몸, 하얀 배, 크고 동그란 눈, 하얀 외뿔, 둥근 등 돌기
ALLY_DNA = (
    "chubby light green dinosaur, large white circular belly patch, "
    "one white horn on head, sequence of white rounded spikes on back, "
    "very large round eyes, 3D Pixar render, masterpiece, vivid colors"
)

# --- 2. 페이지 설정 ---
st.set_page_config(page_title="Ally Studio", page_icon="🦖", layout="centered")

# 디자인 개선
st.markdown("<style>div.stButton > button {width: 100%; border-radius: 10px; height: 3em; background-color: #7ED957; color: white; border: none;}</style>", unsafe_allow_html=True)

st.title("🦖 올리(Ally) 이미지 스튜디오")
st.info("올리의 특징(큰 눈, 하얀 뿔과 배)이 잘 반영된 이미지를 생성합니다.")

# --- 3. 입력창 ---
user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 구름 위에서 잠자는, 친구와 파티하는")

if st.button("✨ 올리 소환하기!"):
    if user_input:
        # 진행 상태 표시
        with st.status("올리가 열심히 그림을 그리고 있어요...", expanded=True) as status:
            seed_num = random.randint(1, 1000000)
            # 프롬프트 조합
            full_prompt = f"Ally the dinosaur {user_input}, {ALLY_DNA}"
            query = urllib.parse.quote(full_prompt)
            
            # 메인 페이지 튕김 방지용 최종 주소
            image_url = f"https://image.pollinations.ai/prompt/{query}.png?width=1024&height=1024&seed={seed_num}&nologo=true"
            
            # 이미지 출력
            st.image(image_url, caption=f"결과: {user_input} 중인 올리", use_container_width=True)
            status.update(label="소환 완료!", state="complete", expanded=False)
            
            # 다운로드 및 링크 공유
            st.link_button("🖼️ 고화질 이미지 저장/확인하기", image_url)
            st.success("그림이 완성되었습니다! 마우스 우클릭으로 저장하세요.")
    else:
        st.warning("내용을 입력해 주세요!")
