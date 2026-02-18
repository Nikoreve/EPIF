import streamlit as st
import json
import os
from streamlit_configuration import page_config as pc

# Page configuration
pc.streamlit_page_config()

# Load glossary data
@st.cache_resource
def load_glossary():
  """ Return the glossary data """
  with open('./data/glossary.json', 'r', encoding="utf-8") as glossary_file:
    return json.load(glossary_file)


# "Risk factors section"
st.header("Risk factors", divider="gray", text_alignment="center")

st.markdown("For clinical risk factors a ***yes*** or ***no*** response is asked for.")
st.markdown("For functional assessments, demographic information and environmental factors of falls, predefined range of values is set.")

st.space()
st.caption("Limitations")
st.markdown(
  body = 
  """The model was trained on data from elderly characteristics. Exclusion criteria (factors) were: <br>
    &nbsp;&nbsp;• No falls the last 12 months<br>
    &nbsp;&nbsp;• Not ambulatory<br>
    &nbsp;&nbsp;• TUG-score value greater than 15<br>
    &nbsp;&nbsp;• Diagnosis with neurodegenerative disease (e.g. Parkinson's disease)<br>
    &nbsp;&nbsp;• Recent stroke<br>
    &nbsp;&nbsp;• Senile dementia (e.g. Mini-Mental State Exam score less than 24)
  """,
  unsafe_allow_html=True)


st.space()
st.space()

st.caption("Interpretation of the risk factors")
glossary = load_glossary()
interpretation_cols = st.columns(2)
incr_value = 0

for row in glossary["interpretation"]:
  if (incr_value%2 == 0):
    with interpretation_cols[0]:
      with st.expander(row["factor"], expanded=False):
        st.markdown(row["description"])
  else:
    with interpretation_cols[1]:
      with st.expander(row["factor"], expanded=False):
        st.markdown(row["description"])
  incr_value += 1

st.space()
st.space()

# "Guidlines of functional and psychological tests" section
st.caption("Instructions to evaluate correctly the functional and psychological assessments")

assessment_names_list = ["BBS", "FICSIT-4", "Short FES-I", "TUG"]

assets_path = "./assets/pdfs/"
folder_files = os.listdir(assets_path) # Get the files of the folder path
pdf_list = [f for f in folder_files if f.lower().endswith('.pdf')] # Filter for files that end with .pdf

# Create the download buttons
for j in range(len(pdf_list)):
  with open(f"{assets_path}{pdf_list[j]}", "rb") as f:
  # Read and return the data of .pdf files
    pdf_data = f.read()
  
  st.download_button(
    label=f"Download :blue-background[{assessment_names_list[j]}] Instructions",
    data=pdf_data,
    file_name=f"{pdf_list[j]}",
    mime="application/pdf",
    key=f"{pdf_list[j]}",
    on_click="ignore",
    type="tertiary",
    icon=":material/download:"
  )