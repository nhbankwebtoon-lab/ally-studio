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
    
    # [해결 1] 404 방지를 위해 모델 이름을 리스트로 시도
    model = None
    for m_name in ['gemini-1.5-flash', 'models/gemini-1.5-flash']:
        try:
            model = genai.GenerativeModel(m_name)
            break
        except:
            continue

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지를 생성하는 중..."):
                try:
                    # [해결 2] 한글을 영어로 변환 (엔진 인식용)
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. Result only.")
                        eng_action = res.text.strip()
                    except:
                        eng_action = "happy lifestyle"

                    # [해결 3] URL 인코딩 (엑박 방지 핵심)
                    # 올리의 외형 특징 고정
                    base_desc = "A cute 3D chubby green dinosaur with one white horn and big eyes"
                    full_prompt = f"{base_desc}, {eng_action}, high quality"
                    
                    # 한글/공백을 인터넷 주소용 코드로 완벽 변환
                    safe_prompt = urllib.parse.quote(full_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=42"

                    # 결과 출력
                    st.success("올리가 화면에 도착했습니다!")
                    st.image(image_url, use_container_width=True)
                    st.caption(f"현재 상황: {user_input}")

                except Exception as e:
                    st.error(f"오류가 발생했습니다. 다시 시도해 주세요.")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
