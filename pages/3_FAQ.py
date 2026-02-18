import streamlit as st
import json

from streamlit_configuration import page_config as pc

# Page configuration
pc.streamlit_page_config("wide")

# Load FAQs data
@st.cache_resource
def load_FAQs():
  """ Return the Frequently Asked Questions & Answers"""
  with open('./data/faqs.json', 'r', encoding="utf-8") as faqs_file:
    return json.load(faqs_file)

faqs = load_FAQs()


# FAQs section
st.header("Frequently Asked Questions", divider="gray", text_alignment="center")

# print(faqs.types)
# Create faqs display page
faqs_type = ""
for i, row in enumerate(faqs):
  if faqs_type != row["type"]:
    # Check if the type of faqs has changed
    faqs_type = row["type"]
    st.space()
    st.caption(faqs_type)
    
  with st.expander(row["question"], expanded=False):
    # Add an exapander for the FAQs + the answer
    st.markdown(row["description"])
    if row.get("items"):
      for item in row["items"]:
        st.write(f"• {item}")