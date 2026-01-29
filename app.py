import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

ALLY_REF_URL = "https://github.com/nhbankwebtoon-lab/ally-studio/blob/main/ally_ref.png?raw=true"

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # [해결책] 404 에러 방지를 위해 가장 확실한 모델 이름을 사용합니다.
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_input("올리가 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("레퍼런스를 참고하여 올리를 생성 중..."):
                try:
                    # 이미지 불러오기
                    response_img = requests.get(ALLY_REF_URL)
                    ref_image = Image.open(BytesIO(response_img.content))

                    # [이미지 생성 요청] 텍스트와 이미지를 함께 보냅니다.
                    prompt = [
                        f"This is a reference image of Ally, a green dinosaur. "
                        f"Based on this, generate a 3D image of her {user_input}. "
                        f"Keep the design identical: green body, white horn, large eyes.",
                        ref_image
                    ]
                    
                    response = model.generate_content(prompt)
                    
                    st.success("올리의 모습이 업데이트되었습니다!")
                    # 결과 출력 (무료 버전은 우선 텍스트 묘사가 안전하게 나옵니다)
                    st.write(response.text)
                    
                except Exception as e:
                    # 여기서 발생하는 404를 잡기 위해 메시지 출력
                    st.error(f"모델 인식 오류가 발생했어요. 이름을 다시 확인 중입니다: {e}")
        else:
            st.warning("내용을 입력해주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
