import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖", layout="centered")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 API 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("API Key를 입력해야 올리가 그림을 그릴 수 있어요!")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # [해결 1] 404 에러 방지용 가장 안정적인 모델 이름 사용
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API 연결에 문제가 있습니다: {e}")

    # 3. 사용자 입력창
    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리를 소환하는 중... 잠시만 기다려 주세요!"):
                try:
                    # [해결 2] 한글 입력을 영어로 강제 변환 (엑박 방지의 핵심)
                    eng_action = "happy and playing" # 기본값 설정
                    try:
                        # Gemini에게 번역을 시킵니다.
                        translation_prompt = f"Translate '{user_input}' to English short phrase for an image prompt. Output ONLY English."
                        response = model.generate_content(translation_prompt)
                        if response.text:
                            eng_action = response.text.strip()
                    except:
                        # 번역 실패 시 기본값(eng_action)을 그대로 사용해 멈춤을 방지
                        pass

                    # [해결 3] 엑박(Broken Image) 방지용 URL 인코딩 (기술적 필살기)
                    # 올리의 고유 특징 고정: 초록 몸, 하얀 뿔 하나, 아주 큰 눈
                    base_ally = "A cute 3D chubby green dinosaur character named Ally with one small white horn on head and very large round eyes"
                    final_prompt = f"{base_ally}, {eng_action}, high quality, 3D render style, bright colors"
                    
                    # 주소창에서 한글/공백을 완벽하게 기계어로 변환하여 엑박을 차단합니다.
                    safe_url_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_url_prompt}?width=1024&height=1024&seed=77&nologo=true"

                    # 4. 최종 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    # 이미지를 화면에 강제로 띄웁니다.
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 올리의 현재 상황: {user_input}")
                    st.balloons() # 성공 축하 효과

                except Exception as e:
                    st.error("그림을 가져오는 엔진에 잠시 문제가 생겼어요. 다시 버튼을 눌러주세요!")
        else:
            st.warning("무엇을 하고 있는지 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에서 Gemini API Key를 먼저 입력해 주세요.")

st.markdown("---")
st.caption("© 2026 Ally Studio - Powered by Google Gemini & Pollinations AI")
