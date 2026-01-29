import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 API 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    # 모델 설정
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.error("API 연결을 확인해주세요.")

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: swimming in the sea")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지를 생성하고 안전하게 가져오는 중..."):
                try:
                    # [핵심 1] 올리 특징 고정 (초록색, 통통함, 하얀 뿔, 아주 큰 눈)
                    ally_desc = "A cute 3D chubby green dinosaur with one white horn and very large round eyes"
                    prompt = f"{ally_desc}, {user_input}, high quality, 3D style"
                    
                    # [핵심 2] 엑박 원천 차단: 이미지를 데이터로 직접 다운로드
                    image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42"
                    response = requests.get(image_url, timeout=15)
                    
                    if response.status_code == 200:
                        img_data = BytesIO(response.content)
                        
                        # 3. 결과 출력
                        st.success("드디어 올리가 도착했습니다!")
                        st.image(img_data, use_container_width=True) # 링크가 아닌 실제 데이터로 표시
                        st.balloons()
                    else:
                        st.error("이미지 서버 응답 지연. 다시 한번 눌러주세요!")

                except Exception as e:
                    st.error("잠시 후 다시 시도해 주세요. 올리가 오고 있습니다!")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 넣어주세요.")
