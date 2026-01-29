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
    # [방어 1] 404 모델 에러 방지
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.error("API 연결 상태를 확인해 주세요.")

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("할당량을 아끼며 올리를 소환 중..."):
                try:
                    # [방어 2] 한글을 영어로 안전하게 변환 (엔진은 영어만 이해합니다)
                    # 할당량이 부족해 번역에 실패하더라도 그림은 나오게 설계했습니다.
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. Output ONLY English.")
                        eng_text = res.text.strip()
                    except:
                        eng_text = "playing happily" 

                    # [방어 3] 엑박 방지 필살기: URL 인코딩 (urllib)
                    # 올리 특징 고정: 초록 몸, 하얀 뿔 하나, 아주 큰 눈 [cite: 2026-01-27]
                    base_ally = "A cute 3D chubby green dinosaur with one white horn and very large eyes"
                    final_prompt = f"{base_ally}, {eng_text}, high quality, 3D style"
                    
                    # 주소창의 한글/공백을 기계어로 변환하여 브라우저가 그림을 즉시 읽게 합니다.
                    safe_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=99"

                    # 3. 최종 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    # 이미지를 화면에 띄웁니다.
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")
                    st.balloons() 

                except Exception as e:
                    st.error("이미지 서버 연결에 실패했습니다. 잠시 후 다시 시도해 주세요.")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 먼저 입력해 주세요.")
