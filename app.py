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
        # [해결 1] 404 에러 방지용 모델 로드 (가장 안정적인 이름 사용)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API 연결에 문제가 있습니다: {e}")

    # 3. 사용자 입력창
    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리가 열심히 그림을 그리고 있어요..."):
                try:
                    # [해결 2] 한글 입력을 영어로 안전하게 변환 (이미지 엔진은 영어를 읽어야 엑박이 안 뜹니다)
                    translation_prompt = f"Translate '{user_input}' to English short phrase for an image prompt. Output only the English text."
                    try:
                        response = model.generate_content(translation_prompt)
                        eng_action = response.text.strip()
                    except:
                        # Gemini 번역 실패 시 기본 동작 설정
                        eng_action = "playing and having fun"

                    # [해결 3] 엑박(Broken Image) 방지용 URL 인코딩
                    # 올리의 특징 고정: 초록 몸, 하얀 뿔 하나, 아주 큰 눈 [cite: 2026-01-27]
                    base_prompt = "A cute 3D chubby green dinosaur character named Ally with one small white horn on head and very large round eyes"
                    final_prompt = f"{base_prompt}, {eng_action}, high quality, 3D animation style"
                    
                    # 주소창에서 한글/공백을 완벽하게 기계어로 변환
                    safe_url_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_url_prompt}?width=1024&height=1024&seed=42&nologo=true"

                    # 4. 최종 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    st.image(image_url, caption=f"결과물: {user_input}", use_container_width=True)
                    st.balloons() # 성공 축하 효과

                except Exception as e:
                    st.error(f"그림을 가져오는 중 오류가 발생했습니다: {e}")
        else:
            st.warning("내용을 먼저 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에서 Gemini API Key를 먼저 입력해 주세요.")

st.markdown("---")
st.caption("© 2026 Ally Studio - Powered by Google Gemini & Pollinations AI")
