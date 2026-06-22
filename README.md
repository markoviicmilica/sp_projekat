# ⚽ Predviđanje ishoda utakmica Svetskog prvenstva

## Opis
Model mašinskog učenja za predviđanje ishoda utakmica Svetskog prvenstva na osnovu istorijskih podataka, Elo rejtinga i statističkih pokazatelja forme reprezentacija. Klasifikuje utakmicu u jednu od tri kategorije: pobeda domaćina, nerešeno ili pobeda gosta.

## Performanse 

| Model | Accuracy | Draw Precision | Draw Recall | Draw F1 | Home Recall | Away Recall |
|---------|---------:|---------:|---------:|---------:|---------:|---------:|
| Logistic Regression | 0.620 | 0.000 | 0.000 | 0.000 | 0.887 | 0.448 |
| Decision Tree | 0.524 | 0.250 | 0.238 | 0.244 | 0.660 | 0.418 |
| Random Forest | 0.568 | 0.288 | 0.500 | 0.365 | 0.596 | 0.552 |
| XGBoost | 0.604 | 0.417 | 0.119 | 0.185 | 0.830 | 0.433 |

Napomena: Prikazani rezultati predstavljaju performanse osnovnih modela pre dodatne optimizacije hiperparametara.

## Najbolji model

Za finalni model izabran je optimizovani Random Forest zbog
najuravnoteženijih performansi između sve tri klase
(pobeda domaćina, nerešeno i pobeda gosta).

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| away_win | 0.54 | 0.57 | 0.55 | 67 |
| draw | 0.35 | 0.40 | 0.38 | 42 |
| home_win | 0.74 | 0.70 | 0.72 | 141 |
| **Accuracy** | | | **0.61** | **250** |
| **Macro avg** | **0.55** | **0.56** | **0.55** | **250** |
| **Weighted avg** | **0.62** | **0.61** | **0.62** | **250** |

Iako u osnovi Logistic Regression ostvaruje nešto veću
ukupnu tačnost, Random Forest značajno bolje
prepoznaje nerešene rezultate.

## Pokretanje
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Struktura
```
SPPROJEKAT/
├── app/
│   ├── streamlit_app.py
│   └── pitch.jpg
├── data/
│   ├── raw/
│   │   ├── matches.csv
│   │   └── eloratings.csv
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
Python, Pandas, NumPy, Scikit-learn, XGBoost, Streamlit, Joblib, Matplotlib

## Autor
Milica Marković RA193/2023

## Datum
Jun 2026.

## Predmet
SAUSAU - Softverski algoritmi u sistemima automatskog upravljanja
