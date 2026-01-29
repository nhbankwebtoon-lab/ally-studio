import streamlit as st
import google.generativeai as genai
import urllib.parse
import requests

st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # [해결 1] 404 에러 방지를 위한 유연한 모델 로드
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
                    # [해결 2] 한글을 영어로 안전하게 변환 (번역 실패 시 기본값 사용)
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. Result only.")
                        eng_action = res.text.strip()
                    except:
                        eng_action = "playing happily"

                    # [해결 3] 이미지 주소 인코딩 (엑박 방지 핵심)
                    # 올리의 외형 특징을 영어로 고정
                    base_desc = "A cute 3D chubby green dinosaur with one white horn and big eyes"
                    full_prompt = f"{base_desc}, {eng_action}, high quality, bright colors"
                    
                    # URL에 쓸 수 없는 문자들을 안전하게 변환
                    encoded_prompt = urllib.parse.quote(full_prompt)
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42"

                    # 4. 결과 출력
                    st.success("올리가 도착했습니다!")
                    st.image(image_url, use_container_width=True)
                    st.caption(f"상태: {user_input}")

                except Exception as e:
                    st.error(f"이미지 표시 중 오류가 발생했습니다. 다시 시도해 주세요.")
        else:
            st.warning("무엇을 하고 있는지 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
