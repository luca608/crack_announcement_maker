import streamlit as st
import google.generativeai as genai

# 1. 화면 설정
st.title("📢 크랙(Crack) 공지사항 생성기")
st.write("운영팀을 위한 AI 에디터입니다. 내용을 입력하면 공지 톤으로 바꿔드려요!")

# 2. 사이드바: API 키 입력
api_key = st.sidebar.text_input("Google API Key를 입력하세요", type="password")

# 3. 입력 양식
with st.form("notice_form"):
    st.subheader("📝 공지 정보 입력")
    
    # 필수 항목
    category = st.selectbox("공지 유형", ["업데이트 (긍정)", "이벤트 (긍정)", "점검 (부정/긴급)", "장애 (부정/긴급)", "일반 안내"])
    content = st.text_area("핵심 내용", height=100, placeholder="예: 내일 새벽 2시 점검함. 서버 안정화 작업.")
    when = st.text_input("일시/기간", placeholder="예: 내일 14:00 ~ 16:00")
    target = st.text_input("대상 (선택)", placeholder="전체 사용자")
    
    submitted = st.form_submit_button("공지사항 생성하기 ✨")

# 4. AI가 글을 쓰는 로직
if submitted:
    if not api_key:
        st.error("API 키를 먼저 입력해주세요!")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-pro-preview')
        
        prompt = f"""
        당신은 서비스 '크랙(Crack)'의 운영팀입니다. 아래 정보를 바탕으로 공지사항을 작성하세요.
        
        [입력 정보]
        - 유형: {category}
        - 핵심 내용: {content}
        - 일시: {when}
        - 대상: {target}
        
        [작성 규칙]
        1. 말투: 전문적이고 정중하지만, '관심과 애정', '너른 양해' 같은 표현으로 친근함을 줄 것.
        2. 구조: 제목, 인삿말, 상세 안내(불렛 포인트), 마무리, 서명 순서.
        3. 시간: 반드시 24시간제(14:00) 사용 및 절대적 날짜/요일로 변환.
        4. 화폐: '크래커' 단위 사용.
        """
        
        with st.spinner("운영자님이 작성 중입니다... ✍️"):
            try:
                response = model.generate_content(prompt)
                st.success("작성 완료!")
                st.markdown(response.text)
                st.info("💡 내용을 복사해서 사용하세요.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
