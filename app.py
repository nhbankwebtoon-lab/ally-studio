import streamlit as st
import google.generativeai as genai
import PIL.Image

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="Ally Studio", page_icon="🦖", layout="centered")
st.title("🦖 올리(Ally) 이미지 스튜디오")
st.markdown("올리가 어떤 상황에 있는지 입력하면 AI가 바로 그려줘요! (무료 버전)")

# 2. 사이드바 - API 키 입력 (보안을 위해 비밀 입력 사용)
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("비용은 발생하지 않으니 안심하세요!")

# 3. 이미지 생성 로직
if api_key:
    genai.configure(api_key=api_key)
    try:
        # 모델 설정 (if문 안으로 들여쓰기 필수)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

    # 사용자 입력창
    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 피자 먹는 모습, 우주복 입은 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리가 그림 그리러 여행 중..."):
                try:
                    # 올리의 정체성을 유지하기 위한 시스템 프롬프트 자동 결합
                    ally_identity = (
                        "Reference Character: 'Ally'. Description: A cute green dinosaur with "
                        "huge round eyes (50% of face), a single white horn on top of the head, "
                        "and a pale-colored chubby belly. 3D Pixar/Disney animation style. "
                    )
                    
                    # 이미지 생성 요청
                    response = model.generate_content([f"{ally_identity} Task: {user_input}"])
                    
                    # 결과 화면 표시 (Gemini 2.0 Native Image Generation 지원 시)
                    # *참고: 현재 API 응답 구조에 따라 이미지/텍스트를 처리합니다.
                    st.success("짠! 올리가 도착했어요!")
                    st.image(response.text) # 생성된 이미지 표시
                except Exception as e:
                    st.error(f"오류가 발생했어요: {e}")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")

st.divider()
st.caption("© 2026 Ally Studio - Powered by Gemini 2.0 Flash")
