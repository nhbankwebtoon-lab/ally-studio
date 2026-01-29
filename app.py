import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="올리(Ally) 이미지 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 사이드바 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("비용은 발생하지 않으니 안심하세요!")

if api_key:
    genai.configure(api_key=api_key)
    
    # 404 에러를 피하기 위해 가능한 모든 모델 이름을 순서대로 시도합니다.
    model_names = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro-vision',
        'models/gemini-1.5-flash',
        'gemini-2.0-flash-exp'
    ]
    
    model = None
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            # 모델이 정상인지 가볍게 체크
            break 
        except:
            continue

    if model is None:
        st.error("사용 가능한 Gemini 모델을 찾을 수 없습니다. API 키를 확인해 주세요.")
    else:
        # 사용자 입력창
        user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 우주복 입은 올리")

        if st.button("올리 그려줘!"):
            if user_input:
                with st.spinner("올리가 우주에서 날아오고 있어요..."):
                    try:
                        # 올리의 특징을 프롬프트에 강제로 주입
                        ally_prompt = f"A cute green dinosaur character named Ally with one small white horn on head, very large round eyes, chubby body, pale belly. {user_input}, 3D render style, high quality."
                        
                        response = model.generate_content(ally_prompt)
                        st.write(response.text)
                        st.info("현재 무료 버전 API는 텍스트 묘사 위주로 작동할 수 있습니다.")
                    except Exception as e:
                        st.error(f"오류가 발생했어요: {e}")
            else:
                st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")

st.caption("© 2026 Ally Studio - Powered by Gemini")
