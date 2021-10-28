import streamlit as st
import os

def set_style(file_name):
    """ Method for reading styles.css and applying necessary changes to HTML """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

