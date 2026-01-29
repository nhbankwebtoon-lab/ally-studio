import streamlit as st
import google.generativeai as genai
import urllib.parse

st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 모델 설정 (최대한 안전한 이름 사용)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: swimming in the sea")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지를 생성 중입니다..."):
                try:
                    # 1. 입력값이 한글일 경우를 대비해 간단하게 영어로 변환 시도
                    # 만약 여기서 404 에러가 나면 except 구문으로 넘어가서 기본값 사용
                    try:
                        response = model.generate_content(f"Translate '{user_input}' to a short English phrase. Result only.")
                        action = response.text.strip()
                    except:
                        action = "happy lifestyle"

                    # 2. 올리의 고정 외형 프롬프트 (영어)
                    # 초록색 공룡, 머리 위 하얀 뿔 하나, 아주 큰 눈, 통통한 몸
                    base_ally = "A cute chubby green dinosaur named Ally with one small white horn on head and very large round eyes"
                    final_prompt = f"{base_ally}, {action}, 3D render, high quality, bright background"

                    # 3. 주소 인코딩 (한글 및 공백 제거 핵심)
                    encoded_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=77&nologo=true"

                    # 4. 이미지 출력
                    st.success("올리가 화면에 도착했습니다!")
                    st.image(image_url, use_container_width=True)
                    st.caption(f"상태: {user_input}")

                except Exception as e:
                    st.error(f"화면 표시 중 오류 발생: {e}")
        else:
            st.warning("내용을 입력해주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해주세요.")
