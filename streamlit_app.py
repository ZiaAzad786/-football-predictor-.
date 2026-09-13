import streamlit as st
import math

st.set_page_config(page_title="پیش‌بینی فوتبال", page_icon="⚽", layout="centered")

st.title("⚽ پیش‌بینی نتیجه فوتبال")
st.write("فقط نام دو تیم را وارد کنید؛ نیازی به Team ID نیست.")

# امتیازهای پایه نمونه برای اجرای فوری برنامه
# بعداً می‌توان این بخش را با مدل/داده واقعی جایگزین کرد.
DEFAULT_RATING = 1500
ratings = {
    "Real Madrid": 1700, "Barcelona": 1680, "Manchester City": 1710,
    "Liverpool": 1660, "Arsenal": 1630, "Bayern Munich": 1690,
    "PSG": 1640, "Inter": 1620, "Juventus": 1580,
    "AC Milan": 1570, "Chelsea": 1580, "Manchester United": 1570,
}

def rating(team):
    key = team.strip()
    return ratings.get(key, DEFAULT_RATING)

def predict(home, away):
    rh, ra = rating(home), rating(away)
    # مزیت میزبانی
    diff = (rh + 60) - ra
    p_home = 1 / (1 + 10 ** (-diff / 400))
    p_away = 1 - p_home
    # احتمال مساوی را از دو احتمال برد کم می‌کنیم و بین سه حالت نرمال می‌کنیم
    draw = 0.24 - abs(diff) / 3000
    draw = max(0.12, min(0.28, draw))
    home_win = p_home * (1 - draw)
    away_win = p_away * (1 - draw)
    total = home_win + draw + away_win
    return home_win/total, draw/total, away_win/total

home = st.text_input("تیم میزبان", placeholder="مثلاً Real Madrid")
away = st.text_input("تیم مهمان", placeholder="مثلاً Barcelona")

if st.button("پیش‌بینی", type="primary", use_container_width=True):
    if not home.strip() or not away.strip():
        st.warning("نام هر دو تیم را وارد کنید.")
    elif home.strip().lower() == away.strip().lower():
        st.warning("دو تیم باید متفاوت باشند.")
    else:
        ph, pd, pa = predict(home, away)
        best = max([(ph, f"برد {home}"), (pd, "مساوی"), (pa, f"برد {away}")])[1]

        st.subheader("نتیجه")
        st.metric("پیش‌بینی اصلی", best)
        c1, c2, c3 = st.columns(3)
        c1.metric(f"برد {home}", f"{ph*100:.1f}%")
        c2.metric("مساوی", f"{pd*100:.1f}%")
        c3.metric(f"برد {away}", f"{pa*100:.1f}%")

        # امتیاز تقریبی برای نمایش ساده
        exp_h = 1.35 + max(0, (rating(home)-rating(away))/1000)
        exp_a = 1.05 + max(0, (rating(away)-rating(home))/1200)
        st.write(f"گل مورد انتظار تقریبی: **{exp_h:.1f} - {exp_a:.1f}**")

st.divider()
st.caption("این نسخه برای اجرای فوری آماده است. برای مدل آماری واقعی، باید داده تاریخی مسابقات یا مدل آموزش‌دیده به برنامه متصل شود.")
