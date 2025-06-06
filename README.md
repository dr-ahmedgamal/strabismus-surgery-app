# Strabismus Surgical Planner App

This Streamlit app helps ophthalmologists plan surgical correction for various types of strabismus.

## Features

- Supports Esotropia, Exotropia, Hypertropia, and Hypotropia.
- Suggests appropriate muscles to operate based on type, deviation, and approach.
- Uses nomograms with precision (0.5 mm steps) up to maximum safe values.
- Provides both unilateral and bilateral surgical plans.

## How to Use

1. Upload the `strabismus_nomogram.csv` file.
2. Choose the type of strabismus, deviation amount, and surgical approach.
3. View surgical recommendations with appropriate muscle actions and measurements.

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## File Descriptions

- `strabismus_nomogram.csv`: Main data file with surgical nomograms.
- `logic.py`: Contains core surgical decision-making logic.
- `app.py`: Main Streamlit app interface.
- `requirements.txt`: Python dependencies.
- `README.md`: App documentation.