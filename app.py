import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import random


st.set_page_config(page_title="Fertility Friend", page_icon="🌸", layout="wide")

#add text
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;  
    }
    </style>
    """, unsafe_allow_html=True)


# Load the CSV data
@st.cache_data
def load_data():
    data = pd.read_csv('cervicalmucus_data.csv')
    return data

cycle_data = load_data()


st.title("🌸 Your Fertility Friend")

st.write(
    """
    The following tool was created using the[What's the cervical mucus method of FAMs? Planned Parenthood Article](https://www.plannedparenthood.org/learn/birth-control/fertility-awareness/whats-cervical-mucus-method-fams).
    """
)

st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="big-font">Discover your cycle with a splash of fun! 🎉</p>', unsafe_allow_html=True)

# # Last period start date input
# last_period = st.date_input("When did your last period start?", datetime.date.today() - datetime.timedelta(days=28))


# # Date input
# today = st.date_input("What's today's date?", datetime.date.today())

# # Calculate cycle day
# cycle_day = (today - last_period).days + 1

# # Display cycle day
# st.subheader(f"🗓️ You're on Day {cycle_day} of your cycle!")

# Mucus input
mucus_options = cycle_data['Cervical Mucus Consistency'].unique()
mucus_emojis = {"Dry": "🏜️", "Sticky": "🍯", "Tacky": "🫱", "Creamy": "🥛", "Stretchy": "🧵", "Very stretchy": "🕸️"}

col1, col2 = st.columns(2)

with col1:
    st.subheader("Yesterday's Mucus Mood")
    mucus_yesterday = st.selectbox("How was your mucus feeling yesterday?", mucus_options, format_func=lambda x: f"{x} {mucus_emojis.get(x, '❓')}")

with col2:
    st.subheader("Today's Mucus Mood")
    mucus_today = st.selectbox("How's your mucus feeling today?", mucus_options, format_func=lambda x: f"{x} {mucus_emojis.get(x, '❓')}")

# Medication input
medication = st.multiselect("Any meds in the mix? 💊", ["None", "Antibiotics", "Hormonal birth control", "Other"])

if st.button("Reveal My Fertility Forecast! 🔮"):
    # Find the closest matching days in the cycle data
    yesterday_match = cycle_data[cycle_data['Cervical Mucus Consistency'] == mucus_yesterday].iloc[0]
    today_match = cycle_data[cycle_data['Cervical Mucus Consistency'] == mucus_today].iloc[0]
    
    # Determine fertility level
    if "Unsafe" in [yesterday_match['Fertility Level'], today_match['Fertility Level']]:
        fertility = "High fertility 🔥"
    elif "Less safe" in [yesterday_match['Fertility Level'], today_match['Fertility Level']]:
        fertility = "Medium fertility 🌱"
    else:
        fertility = "Low fertility ❄️"
    
    st.subheader(f"Your Current Fertility Level: {fertility}")
    
    if medication != ["None"]:
        st.warning("⚠️ Note: Your medication may affect this assessment.")
    
    st.write(f"Yesterday's mucus suggests: {yesterday_match['Additional Notes']}")
    st.write(f"Today's mucus suggests: {today_match['Additional Notes']}")

# Visualize the cycle
st.subheader("Your Cycle Visualized 📊")

fig = px.line(cycle_data, x='Day', y='Fertility Level', color='Phase', 
              hover_data=['Cervical Mucus Consistency', 'Cervical Mucus Color', 'Additional Notes'])
fig.add_vline(x=cycle_day, line_dash="dash", line_color="red", annotation_text="Today")
st.plotly_chart(fig)

st.markdown("---")
st.markdown("**Remember:** This is a fun way to track your cycle, but for serious family planning, always consult a healthcare professional! 👩‍⚕️")

# Fun facts
fun_facts = [
    "Did you know? The word 'mucus' comes from the Latin 'mucus', meaning 'slime' or 'mold'. Lovely! 🤓",
    "Cervical mucus can stretch up to 10cm during your most fertile days. That's as long as a banana! 🍌",
    "Your body produces about 1-2 teaspoons of cervical mucus every day. That's a lot of data! 📊",
    "The pH of cervical mucus changes throughout your cycle. It's like a little science experiment in your body! 🧪"
]

st.subheader("Fun Fact of the Day! 🎈")
st.write(random.choice(fun_facts))
