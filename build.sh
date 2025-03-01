#!/bin/bash

# Run your pre-processing Python script before launching the Streamlit app
python init_db.py

# Launch the Streamlit app
streamlit run app.py
