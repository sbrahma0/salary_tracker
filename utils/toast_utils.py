# utils/toast_utils.py
import streamlit as st
import time

def show_centered_toast(message):
    """Display a custom centered toast message."""
    st.markdown(
        f"""
        <style>
        .centered-toast {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 5px;
            z-index: 1000;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
        }}
        </style>
        <div class="centered-toast">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Automatically remove the toast after 2 seconds
    time.sleep(2)