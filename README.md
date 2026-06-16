# ⚽ SP 2026 - Predviđanje ishoda utakmice

## Opis
Model mašinskog učenja za predviđanje ishoda fudbalskih utakmica na Svetskom prvenstvu 2026. Klasifikuje utakmicu u jednu od tri kategorije: pobeda domaćina, nerešeno ili pobeda gosta.

## Najbolji model
Logistička regresija sa težinom 1.7 za klasu nerešenog ishoda

## Performanse
| Model | Tačnost |
|-------|---------|
| Logistic Regression | 60.80% |
| XGBoost | 60.00% |
| Random Forest | 59.60% |
| Decision Tree | 54.00% |

## Pokretanje
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Struktura
```
SPPROJEKAT/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   │   └── matches.csv
│   └── processed/
│       └── df_final.csv
├── models/
│   ├── final_model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   ├── le_home.pkl
│   └── le_away.pkl
├── projekat.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

## Tehnologije
Python, Scikit-learn, XGBoost, Streamlit, Pandas, NumPy

## Autor
Milica Marković RA193/2023

## Datum
Jun 2026.

## Predmet
SAUSAU - Softverski algoritmi u sistemima automatskog upravljanja