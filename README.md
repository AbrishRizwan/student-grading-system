# 🎓 Student Grading & Performance Analytics System

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)

A Streamlit app that calculates subject-wise grades, overall percentage and GPA from entered marks, and analyses class results from an uploaded CSV file. It is a rule-based tool; no machine learning is used.

🔗 **Live demo:** [Streamlit link]

## Features
**Individual Grading**
- Enter obtained and total marks in an editable table (5 default subjects, rows can be added)
- Generates a report card with overall percentage, GPA and a subject-wise grade breakdown

**Class Analytics (CSV upload)**
- Upload a CSV with `Name` and `Percentage` columns
- Shows class average, highest percentage, number of students passed, and a grade distribution chart

## Grading Scale
Grade boundaries follow the IIUI undergraduate grading scheme.
| Percentage | Grade | GPA |
|---|---|---|
| 80 and above | A | 4.0 |
| 75 to 79 | B+ | 3.5 |
| 70 to 74 | B | 3.0 |
| 65 to 69 | C+ | 2.5 |
| 60 to 64 | C | 2.0 |
| 55 to 59 | D+ | 1.5 |
| 50 to 54 | D | 1.0 |
| Below 50 | F | 0.0 |

GPA is the simple average of subject GPAs. IIUI's official semester GPA is credit-hour weighted, so results can differ when subjects have different credit hours.

## Tech Stack
Python, pandas, Streamlit, Matplotlib

## ⚠️ Limitations
- GPA is an unweighted average of subject GPAs; it does not use credit hours
- The marks input is limited to 0-100 per subject
- The CSV must contain a `Percentage` column with values from 0 to 100

## Repository Structure
```text
├── app.py              # Streamlit application
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Run Locally
```bash
git clone https://github.com/AbrishRizwan/student-grading-system.git
cd student-grading-system
pip install -r requirements.txt
streamlit run app.py
```
