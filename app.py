import streamlit as st

st.set_page_config(page_title="교원 다면평가 점수 계산기", page_icon="📊", layout="centered")

st.title("📊 청량 다면평가 점수 계산기")
st.write(
    """
    항목별로 자신의 상황을 선택하면 자동으로 점수가 계산됩니다.  
    총점은 100점 만점이며, **가산점에 따라 100점을 초과할 수 있습니다.**
    """
)

st.markdown("---")

# =========================
# 유틸 함수들
# =========================

def calc_teaching_hours(
    real_hours: float,
    creative_hours: float,
    homeroom_status: str,
    club_homeroom: bool,
    is_head: bool,
    sports_club: bool,
) -> float:
    """수업 시수 계산"""
    total = real_hours + creative_hours * 0.5

    if homeroom_status == "담임":
        total += 1.0
    elif homeroom_status == "부담임":
        total += 0.5

    if club_homeroom:
        total += 1.0
    if is_head:
        total += 1.0
    if sports_club:
        total += 1.0

    return total


def teaching_hours_to_score(hours: float) -> float:
    """수업 시수를 30점 만점 점수로 변환"""
    if hours >= 18:
        return 30.0
    elif hours >= 17.5:
        return 29.5
    elif hours >= 17:
        return 29.0
    elif hours >= 16.5:
        return 28.5
    elif hours >= 16:
        return 28.0
    elif hours >= 15.5:
        return 27.5
    elif hours >= 15:
        return 27.0
    elif hours >= 14.5:
        return 26.5
    elif hours >= 14:
        return 26.0
    elif hours >= 13.5:
        return 25.5
    elif hours >= 13:
        return 25.0
    elif hours >= 12.5:
        return 24.5
    elif hours >= 12:
        return 24.0
    elif hours >= 11.5:
        return 23.5
    elif hours >= 11:
        return 23.0
    elif hours >= 10.5:
        return 22.5
    else:
        return 22.0


def calc_life_guidance_score() -> float:
    """생활지도(30점) 점수 계산 (단계별 질문 방식)"""
    st.subheader("② 생활지도 (30점)")

    q1 = st.radio("1) 담임인가요?", ("아니요", "예"), key="life_q1")

    if q1 == "예":
        st.info("담임이므로 생활지도 점수는 **30점**입니다.")
        return 30.0

    q2 = st.radio(
        "2) 거점학교, 운동부 담당(정), 보건, 사서, 전문상담, "
        "생활안전부(부장·기획1·기획2)에 해당하나요?",
        ("아니요", "예"),
        key="life_q2",
    )

    if q2 == "예":
        st.info("해당 직무이므로 생활지도 점수는 **26점**입니다.")
        return 26.0

    q3 = st.radio("3) 비담임인가요?", ("아니요", "예"), key="life_q3")

    if q3 == "예":
        st.info("비담임이므로 생활지도 점수는 **22점**입니다.")
        return 22.0

    st.warning("해당되는 항목이 선택되지 않았습니다. 생활지도 점수는 0점으로 계산됩니다.")
    return 0.0


def training_hours_to_score(hours: float) -> float:
    """연수 시간 → 전문성계발(10점) 점수 변환"""
    if hours >= 60:
        return 10.0
    elif hours >= 45:
        return 9.0
    elif hours >= 30:
        return 8.0
    elif hours >= 15:
        return 6.0
    elif hours >= 1:
        return 5.0
    else:
        return 0.0


# =========================
# ① 수업지도 (30점)
# =========================

st.subheader("① 수업지도 (30점)")

st.markdown("**다음 질문에 답하면 수업 시수에 따른 점수가 계산됩니다.**")

col1, col2 = st.columns(2)
with col1:
    real_hours = st.number_input(
        "1) (창체 제외) 실수업 시수 (주당, 시간)",
        min_value=0.0,
        step=0.5,
        value=18.0,
        help="창체를 제외한 실제 교과 수업 시수입니다.",
        key="real_hours",
    )
with col2:
    creative_hours = st.number_input(
        "2) 창체 수업 시수 (주당, 시간)",
        min_value=0.0,
        step=0.5,
        value=0.0,
        key="creative_hours",
    )

homeroom_status = st.radio(
    "3) 담임/부담임 여부",
    ("해당 없음", "담임", "부담임"),
    key="homeroom_status",
)

col3, col4, col5 = st.columns(3)
with col3:
    is_club_homeroom = st.checkbox("4) 동아리 담임", key="club_homeroom")
with col4:
    is_head = st.checkbox("5) 부장교사", key="is_head")
with col5:
    is_sports_club = st.checkbox("6) 스포츠클럽 담임", key="sports_club")

total_hours = calc_teaching_hours(
    real_hours,
    creative_hours,
    homeroom_status,
    is_club_homeroom,
    is_head,
    is_sports_club,
)
teaching_score = teaching_hours_to_score(total_hours)

st.info(f"▶ 계산된 총 시수: **{total_hours:.1f}시간** → 수업지도 점수: **{teaching_score:.1f}점 / 30점**")

st.markdown("---")

# =========================
# ② 생활지도 (30점)
# =========================

life_score = calc_life_guidance_score()

st.markdown("---")

# =========================
# ③ 담당업무 (30점)
# =========================

st.subheader("③ 담당업무 (30점)")

duty_role = st.radio(
    "담당업무에 해당하는 항목을 선택하세요.",
    ("부장교사", "기획/보건/사서/전문상담", "일반계원", "해당 없음"),
    key="duty_role",
)

if duty_role == "부장교사":
    duty_score = 30.0
elif duty_role == "기획/보건/사서/전문상담":
    duty_score = 26.0
elif duty_role == "일반계원":
    duty_score = 22.0
else:
    duty_score = 0.0

st.info(f"▶ 담당업무 점수: **{duty_score:.1f}점 / 30점**")

st.markdown("---")

# =========================
# ④ 전문성계발 (10점)
# =========================

st.subheader("④ 전문성계발 (10점)")

training_hours = st.number_input(
    "연수 이수 시간 (시간 단위)",
    min_value=0.0,
    step=1.0,
    value=0.0,
    key="training_hours",
)

professional_score = training_hours_to_score(training_hours)

st.info(f"▶ 전문성계발 점수: **{professional_score:.1f}점 / 10점**")

st.markdown("---")

# =========================
# ⑤ 가산점
# =========================

st.subheader("⑤ 가산점")

st.write("해당되는 항목에만 체크하세요. (가산점 때문에 총점이 100점을 초과할 수 있습니다.)")

col_b1, col_b2 = st.columns(2)
with col_b1:
    bonus_subject_head = st.checkbox("교과 주임", key="bonus_subject_head")
    bonus_over_18 = st.checkbox("실수업 18시간 초과자 (창체 제외 기준)", key="bonus_over_18")
    bonus_3_subjects = st.checkbox("실수업 교과(창체 제외) 3과목 이상", key="bonus_3_subjects")
    bonus_school_violence = st.checkbox("학교폭력전담기구 위원", key="bonus_school_violence")

with col_b2:
    bonus_hr_committee = st.checkbox("인사자문위원회 위원", key="bonus_hr_committee")
    bonus_school_council = st.checkbox("학교운영위원회 교원위원", key="bonus_school_council")
    bonus_mutual_aid = st.checkbox("상조회 임원(회장, 총무)", key="bonus_mutual_aid")
    bonus_lesson_research = st.checkbox("수업연구(교육부·교육청·지구별 등)", key="bonus_lesson_research")

bonus_score = 0.0
# 각 항목별 가산점 부여
if bonus_subject_head:
    bonus_score += 0.5
if bonus_over_18:
    bonus_score += 0.5
if bonus_3_subjects:
    bonus_score += 0.5
if bonus_school_violence:
    bonus_score += 0.5
if bonus_hr_committee:
    bonus_score += 0.5
if bonus_school_council:
    bonus_score += 1.0
if bonus_mutual_aid:
    bonus_score += 1.0
if bonus_lesson_research:
    bonus_score += 1.0

st.info(f"▶ 가산점 합계: **{bonus_score:.1f}점**")

st.markdown("---")

# =========================
# 최종 점수 계산
# =========================

if st.button("✅ 최종 점수 계산하기"):
    base_total = teaching_score + life_score + duty_score + professional_score
    final_total = base_total + bonus_score

    st.subheader("📌 최종 결과")

    st.write(f"- 수업지도: **{teaching_score:.1f}점**")
    st.write(f"- 생활지도: **{life_score:.1f}점**")
    st.write(f"- 담당업무: **{duty_score:.1f}점**")
    st.write(f"- 전문성계발: **{professional_score:.1f}점**")
    st.write(f"- (소계) 가산점 제외 총점: **{base_total:.1f}점 / 100점**")
    st.write(f"- 가산점: **{bonus_score:.1f}점**")

    st.success(f"🎉 최종 점수: **{final_total:.1f}점** (가산점 포함)")

    if final_total > 100:
        st.caption("※ 가산점으로 인해 100점을 초과했습니다.")


