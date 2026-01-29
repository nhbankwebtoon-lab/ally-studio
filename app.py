import streamlit as st
import google.generativeai as genai
import urllib.parse # 한글 주소 문제를 해결하는 통역사 역할

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    # [방어 1] 모델 설정 오류 방지
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.error("API 연결을 확인해주세요.")

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지를 강제로 불러오는 중..."):
                try:
                    # [방어 2] 할당량 아끼기: 번역 실패 시에도 그림은 나오게 설정
                    eng_text = "happy playing" 
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. ONLY English.")
                        if res.text:
                            eng_text = res.text.strip()
                    except:
                        pass # 할당량 초과 시 기본 영어 문구 사용

                    # [방어 3] 엑박 방지 핵심: 올리 특징 고정 및 URL 안전 변환
                    ally_desc = "A cute 3D chubby green dinosaur with one white horn and large eyes"
                    final_prompt = f"{ally_desc}, {eng_text}, high quality, 3D style"
                    
                    # [필살기] 주소창의 한글/공백을 기계어로 변환 (엑박 탈출 비법)
                    safe_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=123"

                    # 3. 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    # 이미지를 화면에 강제로 렌더링
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")
                    st.balloons() 

                except Exception as e:
                    st.error("서버 연결에 실패했습니다. 잠시 후 다시 눌러주세요!")
        else:
            st.warning("무엇을 그릴지 입력해주세요.")
else:
    st.warning("왼쪽 사이드바에 API Key를 먼저 넣어주세요.")
