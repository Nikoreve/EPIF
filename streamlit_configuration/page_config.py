# Streamlit Configuaration
import streamlit as st

logo_path = "./assets/images/logo/"

def streamlit_page_config(layout = 'centered'):
  st.set_page_config(
    page_title = "EPIF",  
    page_icon = f"{logo_path}epif_logo.jpg",
    layout = layout,
    menu_items={
        'Report a bug': "https://forms.gle/4dpdZujumRUE8gvN8",
        'About': 
      '''
          ### Estimation and Personalised Interventions on :blue[elderly] Fallers (EPIF)
          This application was developed by Nikolas Sarakenidis in the context of his Master's thesis on Department of Information and Electronic Engineering at IHU, on fall-risk prediction and prevention in older adults. Supervisor professor of the project is Panagiotis Adamidis.
          
          The purpose of this project is to assist healthcare professionals, by providing a machine learning-based decision support tool for identifying fall-risk profiles and recommending personalized fall prevention interventions.
        '''
    }
  )