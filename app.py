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
    
    # [해결 1] 404 에러 방지 모델 로드
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영하는 모습")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지 생성 중..."):
                try:
                    # [해결 2] 한글을 영어로 안전하게 변환 (실패 시 기본 영어 문구 사용)
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. Output only English.")
                        eng_action = res.text.strip()
                    except:
                        eng_action = "happy and playing"

                    # [해결 3] 엑박 방지 핵심: 올리의 특징(초록 몸, 하얀 뿔, 큰 눈) 고정 및 URL 인코딩
                    # 사용자님이 알려주신 올리의 특징을 영어로 미리 박아두었습니다.
                    base_ally = "A cute 3D chubby green dinosaur with one small white horn on head and very large round eyes"
                    final_prompt = f"{base_ally}, {eng_action}, high quality, bright colors"
                    
                    # 주소창에서 한글/공백을 완벽하게 기계어로 변환 (이걸 안 하면 엑박이 뜹니다)
                    safe_prompt = urllib.parse.quote(final_prompt)
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=99"

                    # 3. 결과 출력
                    st.success("올리가 도착했습니다!")
                    # 이미지를 먼저 확실히 띄웁니다.
                    st.image(image_url, use_container_width=True)
                    st.info(f"💡 현재 상황: {user_input}")

                except Exception as e:
                    st.error("이미지 서버 연결에 실패했습니다. 다시 시도해 주세요.")
        else:
            st.warning("내용을 입력해주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
