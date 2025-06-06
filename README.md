
# Strabismus Surgical Planner

This app helps ophthalmologists determine surgical plans for strabismus cases based on established surgical nomograms.

## Features
- Covers Esotropia, Exotropia, Hypertropia, Hypotropia, and more
- Handles deviation angles from 15–90 prism diopters in 5 PD steps
- Recommends precise recession/resection procedures based on laterality
- Supports unilateral and bilateral surgical plans

## Usage
To run locally:

1. Install requirements:
    pip install -r requirements.txt

2. Launch the app:
    streamlit run app.py

## Files
- `app.py`: Streamlit app
- `requirements.txt`: Python dependencies
- `strabismus_nomogram_full.csv`: Full surgical reference dataset

## Credits
Developed with ophthalmic surgical principles and literature-based nomograms.
