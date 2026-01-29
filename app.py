import streamlit as st
import urllib.parse

# 1. 고정 데이터 설정 (학습 데이터)
# 공유해주신 올리의 앞/옆/뒤 모습이 담긴 원본 이미지 주소를 여기에 넣으세요.
ALLY_REF_URL = "https://github.com/nhbankwebtoon-lab/ally-studio/blob/main/ally_ref.png?raw=true" 

# 2. 올리의 절대 변하지 않는 외형 특징 (학습용 프롬프트)
ALLY_IDENTITY = (
    "chubby light green dinosaur, large white circular belly patch, "
    "sequence of white rounded spikes on back, very large round eyes, "
    "3D Pixar style render, high quality"
)

def generate_ally_image(user_input):
    # 사용자의 입력값(예: '수영하는')과 올리의 정체성을 결합합니다.
    full_prompt = f"Based on the character design in {ALLY_REF_URL}, draw the dinosaur {user_input}. It must have {ALLY_IDENTITY}."
    
    # URL 인코딩 (한글 입력이나 특수문자 에러 방지)
    encoded_prompt = urllib.parse.quote(full_prompt)
    
    # 최종 생성 주소
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&nologo=true"
    return image_url

# --- UI 부분 ---
st.title("🦖 올리(Ally) 이미지 스튜디오")
user_description = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는, 은행에서 저금하는")

if st.button("올리 그려줘!"):
    with st.spinner("올리가 열심히 준비 중입니다..."):
        final_url = generate_ally_image(user_description)
        
        # 3. 엑박 방지: 이미지를 직접 출력하지 않고 '새 창에서 보기' 링크와 함께 제공
        st.image(final_url, caption="생성된 올리의 모습", use_container_width=True)
        st.markdown(f"[📷 이미지가 안 보인다면 여기서 확인하세요]({final_url})")
        st.info(f"💡 생성된 프롬프트: {user_description}")
