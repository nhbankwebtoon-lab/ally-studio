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
    
    # 모델 로드 (가장 안정적인 방식)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지를 생성하는 중..."):
                try:
                    # 1. 한글 입력을 영어로 변환 (이미지 엔진 인식용)
                    # 만약 Gemini가 응답하지 않을 경우를 대비해 기본값 설정
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to a short English phrase for an image prompt. Result only.")
                        eng_action = res.text.strip()
                    except:
                        eng_action = "happy lifestyle"

                    # 2. 올리의 고정 외형 특징 (영어)
                    base_ally = "A cute 3D chubby green dinosaur with one small white horn and very large round eyes"
                    # 최종 영어 프롬프트 조합
                    final_prompt = f"{base_ally}, {eng_action}, high quality, bright colors"
                    
                    # [핵심] 한글/공백을 안전한 URL 코드로 변환 (엑박 방지)
                    safe_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=42&nologo=true"

                    # 3. 결과 출력
                    st.success("올리가 화면에 도착했습니다!")
                    # 이미지를 먼저 띄웁니다.
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("내용을 입력해주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해주세요.")
