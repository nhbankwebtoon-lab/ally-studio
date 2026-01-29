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
    
    # [방어 1] 404 에러 방지 모델 로드
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리를 소환하는 중..."):
                try:
                    # [방어 2] 한글 입력을 안전한 영어로 강제 변환
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. Output ONLY the English.")
                        eng_action = res.text.strip()
                    except:
                        # Gemini가 죽어도 코드는 멈추지 않음
                        eng_action = "happy playing"

                    # [방어 3] 엑박(Broken Image)의 원인인 한글/공백 완벽 제거
                    # 올리의 외형(초록 몸, 하얀 뿔 하나, 큰 눈)을 영어로 미리 고정 [cite: 2026-01-27]
                    base_prompt = "A cute 3D chubby green dinosaur character with one small white horn on head and very large round eyes"
                    final_prompt = f"{base_ally if 'base_ally' in locals() else base_desc if 'base_desc' in locals() else base_prompt}, {eng_action}, high quality, 3D render style"
                    
                    # URL에 한글이나 공백이 들어가지 않도록 암호화
                    safe_url_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_url_prompt}?width=1024&height=1024&seed=42"

                    # 4. 결과 출력
                    st.success("드디어 올리가 도착했습니다!")
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")

                except Exception as e:
                    st.error("잠시 후 다시 시도해 주세요. 엔진을 점검 중입니다.")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
