import streamlit as st
import google.generativeai as genai
import urllib.parse # 한글 주소 문제를 해결해줄 핵심 도구입니다!

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 API 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    # [방어] 모델 설정
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.error("API 연결을 확인해주세요.")

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 우주복을 입은 올리")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지를 소환하는 중..."):
                try:
                    # [해결 1] 할당량 절약: 번역 실패 시에도 그림은 나오도록 기본값 설정
                    eng_text = "happy playing" 
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. Result ONLY English.")
                        if res.text:
                            eng_text = res.text.strip()
                    except:
                        pass 

                    # [해결 2] 엑박 방지: 올리 특징 고정 및 URL 안전 변환 (URL Encoding)
                    # 초록 몸통, 하얀 뿔 하나, 아주 큰 눈의 특징을 영어로 고정했습니다.
                    base_ally = "A cute 3D chubby green dinosaur character with one small white horn on head and very large round eyes"
                    final_prompt = f"{base_ally}, {eng_text}, high quality, 3D render style"
                    
                    # [핵심] 한글과 공백을 기계가 읽을 수 있는 코드로 변환합니다. (이게 없어서 엑박이 떴던 겁니다!)
                    safe_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=42"

                    # 3. 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    # 이미지를 화면에 띄웁니다.
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")
                    st.balloons() 

                except Exception as e:
                    st.error("이미지 서버가 바빠요. 잠시 후 다시 시도해 주세요!")
        else:
            st.warning("무엇을 그릴지 알려주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 먼저 입력해 주세요.")
