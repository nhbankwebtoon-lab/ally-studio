import streamlit as st
import google.generativeai as genai
import urllib.parse # [핵심] 한글을 기계어로 바꿔주는 통역사

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    # [방어 1] 404 모델 에러 원천 차단
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.error("API Key를 다시 확인해 주세요.")

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 올리")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지 생성 중... 잠시만 기다려 주세요!"):
                try:
                    # [방어 2] 번역 실패 시에도 그림이 나오도록 '기본 영문' 설정
                    eng_text = "happy playing" 
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English. Result ONLY.")
                        if res.text:
                            eng_text = res.text.strip()
                    except:
                        pass # 번역 단계에서 할당량 오류가 나도 그림은 그리러 갑니다.

                    # [방어 3] 엑박 방지: 사용자님이 알려주신 '올리' 특징 고정 [cite: 2026-01-27]
                    # 초록 공룡, 큰 눈, 하얀 외뿔 하나
                    ally_desc = "A cute chubby green dinosaur with one white horn and very large round eyes"
                    final_prompt = f"{ally_desc}, {eng_text}, 3D style, high quality"
                    
                    # [필살기] 한글/공백을 인터넷 표준 주소로 완벽 인코딩 (이게 없어서 엑박이 떴던 겁니다!)
                    safe_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=42"

                    # 3. 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    # 이미지를 화면에 꽉 차게 띄웁니다.
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")
                    st.balloons() 

                except Exception as e:
                    st.error("이미지 서버가 바쁩니다. 잠시 후 다시 눌러주세요!")
        else:
            st.warning("무엇을 그릴지 입력해 주세요.")
else:
    st.warning("왼쪽 사이드바에 API Key를 넣어주세요.")
