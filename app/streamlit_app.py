import streamlit as st
import joblib
import pandas as pd
import numpy as np
import base64

# ============================================================
# KONFIGURACIJA STRANICE
# ============================================================

st.set_page_config(page_title="SP 2026 - Predviđanje", page_icon="⚽")

# ============================================================
# CUSTOM CSS
# ============================================================

try:
    with open('app/pitch.jpg', 'rb') as f:
        img_data = f.read()
    img_base64 = base64.b64encode(img_data).decode()
    bg_style = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;600;700&display=swap');
    
    .stApp {{
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)),
            url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-blend-mode: normal;
    }}
    .main > div {{
        background-color: rgba(0, 0, 0, 0.0);
        border-radius: 20px;
        padding: 20px;
    }}
    h1 {{
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 44px !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #00b894, #00cec9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
        text-align: center;
        margin-bottom: 0px;
    }}
    .subtitle {{
        text-align: center;
        font-size: 18px;
        color: #b2bec3;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 10px;
    }}
    .stSelectbox label, .stNumberInput label {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #dfe6e9 !important;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stSelectbox div, .stNumberInput div {{
        font-size: 16px !important;
        background-color: rgba(255,255,255,0.12) !important;
        border-radius: 8px;
        color: white !important;
    }}
    .stSelectbox div div {{
        color: white !important;
    }}
    .stSelectbox svg {{
        fill: white !important;
    }}
    .stButton button {{
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 14px 30px !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #00b894, #00cec9) !important;
        color: white !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 206, 201, 0.3);
    }}
    .stButton button:hover {{
        transform: scale(1.02);
        transition: 0.2s;
        box-shadow: 0 4px 25px rgba(0, 206, 201, 0.5);
    }}
    .metric-label {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 14px;
        color: #b2bec3 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: center;
    }}
    .metric-value {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 28px;
        color: #ffffff !important;
        text-align: center;
    }}
    .section-title {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 22px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #dfe6e9 !important;
        margin: 20px 0 10px 0;
    }}
    .result-win {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 48px;
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        background: linear-gradient(135deg, #00b89430, #00cec930);
        border: 2px solid #00b894;
        color: #00b894 !important;
        letter-spacing: 3px;
    }}
    .result-lose {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 48px;
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        background: linear-gradient(135deg, #ff767530, #d6303130);
        border: 2px solid #d63031;
        color: #d63031 !important;
        letter-spacing: 3px;
    }}
    .result-draw {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 48px;
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        background: linear-gradient(135deg, #fdcb6e30, #e1705530);
        border: 2px solid #fdcb6e;
        color: #fdcb6e !important;
        letter-spacing: 3px;
    }}
    .prob-label {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 16px;
        text-align: center;
        color: #b2bec3 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .prob-value {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 38px;
        text-align: center;
    }}
    .prob-home {{ color: #55efc4 !important; }}
    .prob-draw {{ color: #fdcb6e !important; }}
    .prob-away {{ color: #ff7675 !important; }}
    .error-text {{
        font-family: 'Orbitron', sans-serif !important;
        font-size: 20px !important;
        color: #ff7675 !important;
        text-align: center !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        padding: 15px !important;
        background: rgba(214, 48, 49, 0.12) !important;
        border-radius: 12px !important;
        border: 2px solid #d63031 !important;
    }}
    .stSpinner > div {{
        color: white !important;
    }}
    hr {{
        border-color: rgba(255,255,255,0.08) !important;
        margin: 15px 0 !important;
    }}
    </style>
    """
except:
    bg_style = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a18, #12122a, #0a0a20);
    }
    .main > div {
        background-color: rgba(0, 0, 0, 0.0);
        border-radius: 20px;
        padding: 20px;
    }
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 44px !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #00b894, #00cec9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #b2bec3;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 10px;
    }
    .stSelectbox label, .stNumberInput label {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #dfe6e9 !important;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stSelectbox div, .stNumberInput div {
        font-size: 16px !important;
        background-color: rgba(255,255,255,0.12) !important;
        border-radius: 8px;
        color: white !important;
    }
    .stSelectbox div div {
        color: white !important;
    }
    .stSelectbox svg {
        fill: white !important;
    }
    .stButton button {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 14px 30px !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #00b894, #00cec9) !important;
        color: white !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 206, 201, 0.3);
    }
    .stButton button:hover {
        transform: scale(1.02);
        transition: 0.2s;
        box-shadow: 0 4px 25px rgba(0, 206, 201, 0.5);
    }
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 14px;
        color: #b2bec3 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: center;
    }
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 28px;
        color: #ffffff !important;
        text-align: center;
    }
    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 22px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #dfe6e9 !important;
        margin: 20px 0 10px 0;
    }
    .result-win {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 48px;
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        background: linear-gradient(135deg, #00b89430, #00cec930);
        border: 2px solid #00b894;
        color: #00b894 !important;
        letter-spacing: 3px;
    }
    .result-lose {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 48px;
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        background: linear-gradient(135deg, #ff767530, #d6303130);
        border: 2px solid #d63031;
        color: #d63031 !important;
        letter-spacing: 3px;
    }
    .result-draw {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 48px;
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        background: linear-gradient(135deg, #fdcb6e30, #e1705530);
        border: 2px solid #fdcb6e;
        color: #fdcb6e !important;
        letter-spacing: 3px;
    }
    .prob-label {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 16px;
        text-align: center;
        color: #b2bec3 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .prob-value {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 38px;
        text-align: center;
    }
    .prob-home {{ color: #55efc4 !important; }}
    .prob-draw {{ color: #fdcb6e !important; }}
    .prob-away {{ color: #ff7675 !important; }}
    .error-text {{
        font-family: 'Orbitron', sans-serif !important;
        font-size: 20px !important;
        color: #ff7675 !important;
        text-align: center !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        padding: 15px !important;
        background: rgba(214, 48, 49, 0.12) !important;
        border-radius: 12px !important;
        border: 2px solid #d63031 !important;
    }}
    .stSpinner > div {{
        color: white !important;
    }}
    hr {{
        border-color: rgba(255,255,255,0.08) !important;
        margin: 15px 0 !important;
    }}
    </style>
    """

st.markdown(bg_style, unsafe_allow_html=True)

# ============================================================
# UČITAVANJE MODELA
# ============================================================

@st.cache_resource
def load_model():
    model = joblib.load('models/final_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    label_encoder = joblib.load('models/label_encoder.pkl')
    le_home = joblib.load('models/le_home.pkl')
    le_away = joblib.load('models/le_away.pkl')
    return model, scaler, label_encoder, le_home, le_away

model, scaler, label_encoder, le_home, le_away = load_model()

@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/jfjelstul/worldcup/master/data-csv/matches.csv')
    df['match_date'] = pd.to_datetime(df['match_date'])
    return df

df = load_data()

# ============================================================
# TIMOVI
# ============================================================

teams = [
    'United States', 'Canada', 'Mexico', 'Panama', 'Haiti', 'Curaçao',
    'Argentina', 'Brazil', 'Uruguay', 'Colombia', 'Ecuador', 'Paraguay',
    'Spain', 'England', 'France', 'Germany', 'Netherlands', 'Portugal',
    'Belgium', 'Croatia', 'Switzerland', 'Austria', 'Norway', 'Scotland',
    'Sweden', 'Turkey', 'Czech Republic', 'Bosnia and Herzegovina',
    'Morocco', 'Senegal', 'Egypt', 'Ivory Coast', 'Algeria', 'South Africa',
    'Ghana', 'Tunisia', 'Cape Verde',
    'Japan', 'Iran', 'South Korea', 'Australia', 'Qatar', 'Saudi Arabia',
    'Iraq', 'Uzbekistan', 'Jordan', 'New Zealand'
]

def safe_encode(team, encoder):
    try:
        return encoder.transform([team])[0]
    except ValueError:
        return 50

stage_map = {
    "Grupna faza": 0,
    "Osmina finala": 1,
    "Cetvrtfinale": 2,
    "Polufinale": 3,
    "Finale": 4
}

def get_fifa_rank_diff(home_team, away_team):
    fifa_ranks = {
        'Argentina': 1, 'Spain': 2, 'France': 3, 'England': 4, 'Portugal': 5,
        'Brazil': 6, 'Morocco': 7, 'Netherlands': 8, 'Belgium': 9, 'Germany': 10,
        'Croatia': 11, 'Colombia': 13, 'Senegal': 14, 'Mexico': 15, 'Uruguay': 16,
        'United States': 17, 'Japan': 18, 'Switzerland': 19, 'Iran': 20,
        'South Korea': 21, 'Australia': 22, 'Canada': 23, 'Ecuador': 27,
        'Ghana': 26, 'Cape Verde': 28, 'Curaçao': 82, 'Haiti': 83,
        'New Zealand': 85, 'Panama': 45, 'Paraguay': 35, 'Austria': 24,
        'Norway': 31, 'Scotland': 40, 'Sweden': 28, 'Turkey': 32,
        'Czech Republic': 38, 'Bosnia and Herzegovina': 55, 'Egypt': 29,
        'Ivory Coast': 33, 'Algeria': 30, 'South Africa': 60, 'Tunisia': 44,
        'Qatar': 50, 'Saudi Arabia': 48, 'Iraq': 70, 'Uzbekistan': 75, 'Jordan': 80
    }
    home_rank = fifa_ranks.get(home_team, 50)
    away_rank = fifa_ranks.get(away_team, 50)
    return home_rank - away_rank

def get_form(team_name, n_matches=3):
    team_matches = df[(df['home_team_name'] == team_name) | (df['away_team_name'] == team_name)]
    team_matches = team_matches.sort_values('match_date', ascending=False).head(n_matches)
    if len(team_matches) == 0:
        return 1.0
    goals = []
    for _, match in team_matches.iterrows():
        if match['home_team_name'] == team_name:
            goals.append(match['home_team_score'])
        else:
            goals.append(match['away_team_score'])
    return sum(goals) / len(goals)

def get_head_to_head(home_team, away_team):
    matches = df[((df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)) |
                 ((df['home_team_name'] == away_team) & (df['away_team_name'] == home_team))]
    home_wins = 0
    for _, match in matches.iterrows():
        if match['result'] == 'home team win' and match['home_team_name'] == home_team:
            home_wins += 1
        elif match['result'] == 'away team win' and match['away_team_name'] == home_team:
            home_wins += 1
    return home_wins

# ============================================================
# UI
# ============================================================

st.markdown("<h1>SP 2026</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Predviđanje ishoda utakmice</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    home = st.selectbox("Domaćin", sorted(teams))
with col2:
    away = st.selectbox("Gost", sorted(teams))

stage = st.selectbox("Faza takmičenja", list(stage_map.keys()), index=0)

if st.button("Predvidi ishod", type="primary", use_container_width=True):
    if home == away:
        st.markdown("<p class='error-text'>Domaćin i gost moraju biti različiti!</p>", unsafe_allow_html=True)
    else:
        with st.spinner("Računam parametre..."):
            head_to_head = get_head_to_head(home, away)
            fifa_diff = get_fifa_rank_diff(home, away)
            home_form = get_form(home)
            away_form = get_form(away)
            stage_encoded = stage_map[stage]
            home_encoded = safe_encode(home, le_home)
            away_encoded = safe_encode(away, le_away)
            
            st.markdown("---")
            st.markdown("<p class='section-title'>Izračunati parametri utakmice</p>", unsafe_allow_html=True)
            
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.markdown("<p class='metric-label'>Forma domaćina</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{home_form:.2f} gol/ut</p>", unsafe_allow_html=True)
            with col_b:
                st.markdown("<p class='metric-label'>Forma gosta</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{away_form:.2f} gol/ut</p>", unsafe_allow_html=True)
            with col_c:
                st.markdown("<p class='metric-label'>Head-to-head</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{head_to_head} pobeda</p>", unsafe_allow_html=True)
            with col_d:
                st.markdown("<p class='metric-label'>FIFA rank razlika</p>", unsafe_allow_html=True)
                color = "#ff7675" if fifa_diff < 0 else "#55efc4"
                st.markdown(f"<p class='metric-value' style='color:{color};'>{fifa_diff}</p>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            input_data = pd.DataFrame([[
                2026, head_to_head, fifa_diff, home_form, away_form,
                stage_encoded, home_encoded, away_encoded
            ]], columns=[
                'year', 'head_to_head', 'fifa_rank_diff', 'home_form_total',
                'away_form_total', 'stage_encoded', 'home_team_encoded', 'away_team_encoded'
            ])
            
            input_scaled = scaler.transform(input_data)
            pred = model.predict(input_scaled)[0]
            result = label_encoder.inverse_transform([pred])[0]
            
            result_map = {
                'home team win': ('POBEDA DOMAĆINA', 'result-win'),
                'away team win': ('POBEDA GOSTA', 'result-lose'),
                'draw': ('NEREŠENO', 'result-draw')
            }
            
            result_text, result_class = result_map[result]
            st.markdown(f"<p class='{result_class}'>{result_text}</p>", unsafe_allow_html=True)
            
            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(input_scaled)[0]
                st.markdown("<p class='section-title'>Verovatnoće ishoda</p>", unsafe_allow_html=True)
                
                col1p, col2p, col3p = st.columns(3)
                with col1p:
                    st.markdown("<p class='prob-label'>Pobeda domaćina</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='prob-value prob-home'>{probs[2]:.1%}</p>", unsafe_allow_html=True)
                with col2p:
                    st.markdown("<p class='prob-label'>Nerešeno</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='prob-value prob-draw'>{probs[1]:.1%}</p>", unsafe_allow_html=True)
                with col3p:
                    st.markdown("<p class='prob-label'>Pobeda gosta</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='prob-value prob-away'>{probs[0]:.1%}</p>", unsafe_allow_html=True)