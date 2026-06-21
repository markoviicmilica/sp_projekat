import streamlit as st
import joblib
import pandas as pd
import numpy as np
import base64


st.set_page_config(page_title="SP 2026 - Predviđanje", page_icon="⚽")

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

# UČITAVANJE MODELA
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

# Elo
@st.cache_data
def compute_elo_history():
    url_results = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
    df_results = pd.read_csv(url_results)
    df_results['date'] = pd.to_datetime(df_results['date'])
    df_results = df_results.sort_values('date').reset_index(drop=True)

    K = 20
    HOME_ADV = 100
    elo = {}
    elo_history = []

    def get_elo(team):
        return elo.get(team, 1500.0)

    for row in df_results.itertuples():
        home_t, away_t = row.home_team, row.away_team
        home_score, away_score = row.home_score, row.away_score
        date = row.date

        elo_home, elo_away = get_elo(home_t), get_elo(away_t)
        expected_home = 1 / (1 + 10 ** ((elo_away - (elo_home + HOME_ADV)) / 400))

        if home_score > away_score:
            actual_home = 1.0
        elif home_score == away_score:
            actual_home = 0.5
        else:
            actual_home = 0.0

        new_elo_home = elo_home + K * (actual_home - expected_home)
        new_elo_away = elo_away + K * ((1 - actual_home) - (1 - expected_home))
        elo[home_t] = new_elo_home
        elo[away_t] = new_elo_away
        elo_history.append((home_t, date, new_elo_home))
        elo_history.append((away_t, date, new_elo_away))

    df_elo = pd.DataFrame(elo_history, columns=['team_name', 'date', 'elo']).sort_values('date')
    elo_by_team_ = {team: g for team, g in df_elo.groupby('team_name')}
    return elo_by_team_, df_results

elo_by_team, df_results_raw = compute_elo_history()

# Mapiranje imena timova
team_name_map = {
    'South Korea': 'South Korea',
    'IR Iran': 'Iran',
    'United States': 'United States',
}

def get_current_elo(team_name):
    mapped = team_name_map.get(team_name, team_name)
    g = elo_by_team.get(mapped)
    if g is None or len(g) == 0:
        return 1500.0
    return g.iloc[-1]['elo']

def get_fifa_rank_diff(home_team, away_team):
    return get_current_elo(home_team) - get_current_elo(away_team)

# Prijateljske
@st.cache_data
def load_friendly_data():
    return df_results_raw[df_results_raw['tournament'] == 'Friendly'].copy()

df_friendly = load_friendly_data()

team_mapping = {
    'USA': 'United States', 'United States': 'United States',
    'Korea Republic': 'South Korea', 'South Korea': 'South Korea',
    'IR Iran': 'Iran', 'Iran': 'Iran',
}

def get_form(team_name, in_tournament_override=0.0, n_matches=3):
    mapped_team = team_mapping.get(team_name, team_name)

    home_m = df_friendly[df_friendly['home_team'] == mapped_team].copy()
    home_m['goals'] = home_m['home_score']
    away_m = df_friendly[df_friendly['away_team'] == mapped_team].copy()
    away_m['goals'] = away_m['away_score']

    all_m = pd.concat([home_m, away_m]).sort_values('date', ascending=False).head(n_matches)
    friendly_form = all_m['goals'].mean() if len(all_m) > 0 else 0.0

    return in_tournament_override * 0.7 + friendly_form * 0.3


# Timovi
teams = [
    'United States', 'Canada', 'Mexico', 'Panama', 'Haiti', 'Curaçao',
    'Argentina', 'Brazil', 'Uruguay', 'Colombia', 'Ecuador', 'Paraguay',
    'Spain', 'England', 'France', 'Germany', 'Netherlands', 'Portugal',
    'Belgium', 'Croatia', 'Switzerland', 'Austria', 'Norway', 'Scotland',
    'Sweden', 'Turkey', 'Czech Republic', 'Bosnia and Herzegovina',
    'Morocco', 'Senegal', 'Egypt', 'Ivory Coast', 'Algeria', 'South Africa',
    'Ghana', 'Tunisia', 'Cape Verde', 'DR Congo',
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
    "Osmina finala": 3,
    "Cetvrtfinale": 4,
    "Polufinale": 1,
    "Finale": 2
}

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


# UI
st.markdown("<h1>SP 2026</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Predviđanje ishoda utakmice</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    home = st.selectbox("Domaćin", sorted(teams))
with col2:
    away = st.selectbox("Gost", sorted(teams))

stage = st.selectbox("Faza takmičenja", list(stage_map.keys()), index=0)

col3, col4 = st.columns(2)
with col3:
    home_goals_input = st.number_input("Golovi domaćina", min_value=0, value=0, step=1)
with col4:
    away_goals_input = st.number_input("Golovi gosta", min_value=0, value=0, step=1)
if st.button("Predvidi ishod", type="primary", use_container_width=True):
    if home == away:
        st.markdown("<p class='error-text'>Domaćin i gost moraju biti različiti!</p>", unsafe_allow_html=True)
    else:
        with st.spinner("Računam parametre..."):
            head_to_head = get_head_to_head(home, away)
            fifa_diff = get_fifa_rank_diff(home, away)
            home_form = get_form(home, in_tournament_override=home_goals_input)
            away_form = get_form(away, in_tournament_override=away_goals_input)
            stage_encoded = stage_map[stage]
            home_encoded = safe_encode(home, le_home)
            away_encoded = safe_encode(away, le_away)

            st.markdown("---")
            st.markdown("<p class='section-title'>Izračunati parametri utakmice</p>", unsafe_allow_html=True)

            home_form_display = home_form / 0.3 if home_goals_input == 0 else home_form
            away_form_display = away_form / 0.3 if away_goals_input == 0 else away_form

            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.markdown("<p class='metric-label'>Forma domaćina</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{home_form_display:.2f} gol/ut</p>", unsafe_allow_html=True)
            with col_b:
                st.markdown("<p class='metric-label'>Forma gosta</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{away_form_display:.2f} gol/ut</p>", unsafe_allow_html=True)
            with col_c:
                st.markdown("<p class='metric-label'>Head-to-head</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{head_to_head} pobeda</p>", unsafe_allow_html=True)
            with col_d:
                st.markdown("<p class='metric-label'>Elo razlika</p>", unsafe_allow_html=True)
                color = "#ff7675" if fifa_diff < 0 else "#55efc4"
                st.markdown(f"<p class='metric-value' style='color:{color};'>{fifa_diff:.0f}</p>", unsafe_allow_html=True)

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