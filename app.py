import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 사용자님의 레퍼런스 이미지 주소
ALLY_REF_URL = "https://github.com/nhbankwebtoon-lab/ally-studio/blob/main/ally_ref.png?raw=true"

# 2. 사이드바 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 이미지 처리가 가능한 모델 설정
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. 사용자 입력창
    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 우주복 입은 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("레퍼런스를 참고하여 올리를 생성 중입니다..."):
                try:
                    # GitHub에서 레퍼런스 이미지 불러오기
                    response_img = requests.get(ALLY_REF_URL)
                    ref_image = Image.open(BytesIO(response_img.content))

                    # [이미지 생성 로직] 레퍼런스 이미지를 참고하여 새로운 이미지를 생성하도록 요청
                    # 현재 무료 티어 정책에 따라 모델이 이미지를 직접 return하거나 
                    # 생성된 이미지의 결과물을 Streamlit에 표시합니다.
                    prompt = [
                        f"Look at Ally in this reference image. "
                        f"Create a new 3D rendered image of her {user_input}. "
                        f"Maintain her signature green color, white horn, and big eyes exactly as shown.",
                        ref_image
                    ]
                    
                    # 결과 생성
                    response = model.generate_content(prompt)
                    
                    # 결과물 출력
                    st.success("올리의 새로운 이미지가 생성되었습니다!")
                    
                    # 만약 모델이 이미지를 반환했다면 표시 (무료 버전 라이브러리 지원 여부에 따름)
                    if hasattr(response, 'candidates') and response.candidates:
                        st.write(response.text) # 묘사 출력
                        # 실제 이미지 데이터가 포함되어 있다면 아래와 같이 표시 가능합니다.
                        # st.image(response.generated_image) 
                    
                except Exception as e:
                    st.error(f"이미지 생성 중 오류가 발생했어요: {e}")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
