import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.error("API 연결을 확인해주세요.")

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: swimming in the sea")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리를 소환하는 중..."):
                try:
                    # [비법 1] 사용자 입력어를 무조건 영어로 안전하게 변환
                    # Gemini가 오늘 할당량을 다 썼을 경우를 대비해 예외 처리
                    eng_text = user_input
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. ONLY English.")
                        if res.text:
                            eng_text = res.text.strip()
                    except:
                        pass 

                    # [비법 2] 올리의 특징을 고정하여 퀄리티 보장
                    ally_desc = "A cute 3D chubby green dinosaur with one white horn and large eyes"
                    final_prompt = f"{ally_desc}, {eng_text}, high quality, 3D style"
                    
                    # [핵심 필살기] 공백을 '+'로 바꿔서 브라우저가 인식 못하는 문제를 해결합니다!
                    safe_prompt = final_prompt.replace(" ", "+")
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=2026"

                    # 3. 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    # 엑박 방지를 위해 이미지를 강제로 새로고침하는 인자 추가
                    st.image(image_url, use_container_width=True)
                    st.caption(f"💡 생성된 키워드: {final_prompt}")
                    st.balloons()

                except Exception as e:
                    st.error("이미지 소환 실패. 버튼을 다시 한번 눌러주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 먼저 넣어주세요.")
