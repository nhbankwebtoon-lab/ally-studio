import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. 페이지 설정
st.set_page_config(page_title="올리 스튜디오", page_icon="🦖")
st.title("🦖 올리(Ally) 이미지 스튜디오")

# 2. 사이드바 API Key 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    # [방어 1] 모델 로드 최적화
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_input("올리가 지금 무엇을 하고 있나요?", placeholder="예: 바다에서 수영")

    if st.button("올리 그려줘!"):
        if user_input:
            with st.spinner("이미지 생성 중..."):
                try:
                    # [방어 2] 한글을 영어로 번역 (엔진은 영어만 이해합니다)
                    # 번역이 실패해도 'happy'라는 기본값을 써서 에러를 막습니다.
                    try:
                        res = model.generate_content(f"Translate '{user_input}' to English short phrase. Result ONLY.")
                        eng_text = res.text.strip()
                    except:
                        eng_text = "happy playing"

                    # [핵심] 올리의 특징(초록 몸, 하얀 뿔, 큰 눈) 고정
                    # 한글/공백이 주소에 들어가지 않도록 'quote' 함수로 완전히 감쌉니다.
                    final_prompt = f"A cute 3D chubby green dinosaur with one white horn and large eyes, {eng_text}"
                    safe_prompt = urllib.parse.quote(final_prompt)
                    
                    # 엑박 방지를 위한 최종 URL 생성
                    image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed=42"

                    # 3. 화면 출력
                    st.success("드디어 올리가 도착했습니다!")
                    # use_container_width=True를 사용하여 이미지를 꽉 차게 띄웁니다.
                    st.image(image_url, use_container_width=True)
                    st.info(f"현재 상황: {user_input}")

                except Exception as e:
                    st.error("잠시 후 다시 시도해 주세요.")
        else:
            st.warning("내용을 입력해 주세요!")
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해 주세요.")
