import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("비용은 발생하지 않으니 안심하세요!")

if api_key:
    genai.configure(api_key=api_key)
    
    # [핵심] 404 에러 해결을 위해 사용 가능한 모델을 자동으로 찾는 로직
    try:
        # 시스템에 등록된 모델 중 'generateContent'가 가능한 모델 하나를 자동으로 선택
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            model = genai.GenerativeModel(available_models[0])
        else:
            model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. 사용자 입력창
    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 우주복 입은 올리")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("올리가 우주에서 응답을 준비 중입니다..."):
                try:
                    # 올리의 특징을 텍스트로 생생하게 묘사하도록 요청
                    prompt = f"Describe a cute green dinosaur named Ally with a white horn, large eyes, wearing {user_input} in detail."
                    response = model.generate_content(prompt)
                    
                    st.success("올리가 우주에서 메시지를 보냈어요!")
                    st.write(response.text)
                    st.info("💡 참고: 무료 API 정책으로 인해 현재는 상세한 텍스트 묘사로 제공됩니다.")
                except Exception as e:
                    st.error(f"오류가 발생했어요: {e}")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")

st.caption("© 2026 Ally Studio - Powered by Gemini")
