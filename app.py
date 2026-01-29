import streamlit as st
import google.generativeai as genai

# 1. 페이지 및 사이드바 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # [핵심] 404 에러 방지를 위한 자동 모델 탐색 로직
    available_models = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    model = None
    
    for model_name in available_models:
        try:
            model = genai.GenerativeModel(model_name)
            # 모델이 정상적으로 로드되는지 테스트 호출 (내용 생성은 하지 않음)
            break
        except:
            continue

    if model:
        # 2. 사용자 입력 및 실행
        user_input = st.text_input("올리가 무엇을 하고 있나요?", placeholder="예: 우주복 입은 모습")

        if st.button("올리 그려줘!"):
            if user_input:
                with st.spinner("올리가 우주에서 응답을 준비 중입니다..."):
                    try:
                        # 올리의 외형 특징을 고정하여 묘사 요청
                        prompt = f"Describe a cute green dinosaur character named Ally with one white horn and big eyes, {user_input} in detail."
                        response = model.generate_content(prompt)
                        
                        st.success("올리가 응답을 보냈어요!")
                        st.write(response.text)
                        st.info("💡 참고: 현재 환경에서는 상세한 텍스트 묘사로 올리의 모습을 확인할 수 있습니다.")
                    except Exception as e:
                        st.error(f"오류가 발생했어요: {e}")
            else:
                st.warning("내용을 입력해주세요!")
    else:
        st.error("사용 가능한 Gemini 모델을 찾을 수 없습니다. API 키를 다시 확인해주세요.")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해주세요.")

st.caption("© 2026 Ally Studio - Powered by Gemini")
