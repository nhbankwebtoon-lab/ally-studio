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
    genai.configure(api_key=api_key)
    
    # 404 에러 방지용 모델 설정
    try:
        # 현재 환경에서 가장 인식률이 높은 이름 형식입니다.
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')

    # 3. 사용자 입력
    user_input = st.text_input("올리가 무엇을 하고 있나요?", placeholder="예: 우주복 입은 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리를 부르는 중..."):
                try:
                    # 올리의 특징을 고정하여 묘사 요청
                    prompt = f"Describe a cute green dinosaur named Ally with a white horn, large eyes, wearing {user_input} in detail."
                    response = model.generate_content(prompt)
                    
                    st.success("올리가 우주에서 응답을 보냈어요!")
                    st.write(response.text)
                    st.info("💡 참고: 현재 무료 API 정책으로 인해 이미지는 텍스트 묘사로 제공됩니다.")
                except Exception as e:
                    st.error(f"오류가 발생했어요: {e}")
        else:
            st.warning("내용을 입력해주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해주세요.")
