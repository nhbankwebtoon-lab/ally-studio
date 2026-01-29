import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 API 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    # [방어 1] 모델 지원 에러(404) 방지
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error("API 연결을 확인해주세요.")

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지를 소환하는 중..."):
                try:
                    # [방어 2] 할당량 부족으로 번역 실패 시에도 그림이 나오도록 설정
                    eng_text = "happy playing" 
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. Output ONLY English.")
                        if res.text:
                            eng_text = res.text.strip()
                    except:
                        pass # 번역 에러 시 기본값 사용

                    # [방어 3] 엑박 방지 핵심: 올리 특징 고정 및 URL 인코딩 [cite: 2026-01-27]
                    # 올리 외형: 초록 몸통, 머리 위 하얀 뿔 하나, 아주 큰 눈
                    base_prompt = "A cute 3D chubby green dinosaur character named Ally with one small white horn on head and very large round eyes"
                    final_prompt = f"{base_prompt}, {eng_text}, high quality, 3D style"
                    
                    # [필살기] 한글과 공백을 기계어로 변환하여 브라우저가 즉시 읽게 함
                    safe_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=123"

                    # 3. 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    # 이미지를 화면에 강제로 띄움
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")
                    st.balloons() 

                except Exception as e:
                    st.error("잠시 후 다시 시도해 주세요.")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("사이드바에 API Key를 입력해 주세요.")
