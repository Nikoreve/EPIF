import streamlit as st
from streamlit_configuration import page_config as pc

# Page configuration
pc.streamlit_page_config("wide")

# Load overall summary data
@st.cache_resource
def load_overall_summary():
  file_name = 'overall_summary.txt'
  with open(f"data/summary/{file_name}", "r", encoding='utf-8') as overall_sum_file:
    return overall_sum_file.read()

# Load clusters/risk-profiles summary data
@st.cache_resource
def load_clusters_summary():
  files = []
  for i in range(3):
    file_name = f"cluster_summary_{i}.txt"
    with open(f'data/summary/{file_name}', "r", encoding='utf-8') as f:
      files.append(f.read())
  return files


overall_sum_file = load_overall_summary() # an instance
clusters_summary = load_clusters_summary() # 3 instances, it's a list

# "Data summary" section
st.header("Data summary")

st.space()
st.caption("Notes")
st.markdown(
  ''' 
      **(M)**:  Mean value of the group
  
      **(SD)**: Standard deviation of the group
      
      **(%)**:    Percentage of the group, which implies if the disease is present or assessment has been done (based on the feature)
  '''
)

# Tab section
st.space()
tabs = st.tabs(['Overall Summary', 'Profiles Summary'])


cluster_title = ["Low Risk Profile", "Moderate Risk Profile", "High Risk Profile"]
with tabs[0]:
  cols = st.columns([1,1,1], vertical_alignment="center")
  with cols[1]:
    container = st.container(width='stretch', height=490,  border=True) 
    with container:
      st.subheader('Overall')
      st.markdown(f'{overall_sum_file}', unsafe_allow_html=True)
with tabs[1]:
  cols = st.columns(3, gap='medium', vertical_alignment='center', border=True)
  for i in range(3):
    with cols[i]:
      container = st.container(width='stretch',height=490, border=False)
      with container:
        st.subheader(f'{cluster_title[i]}')
        st.markdown(f'{clusters_summary[i]}', unsafe_allow_html=True)


st.space()
st.space()
st.subheader("Features contribution per profile")


# st.caption("Importance information")
with st.expander("Important information about charts", expanded=False, icon=":material/notes:"):
  st.markdown('''
    **X-axis**: Represents the mean of SHAP value. It shows the average impact of each feature on the profile
  
    **Y-axis**: Shows the top-14 most impactful features on the profile. The rest are gathered in the last bar
  
    **Bars**: The length of each bar corresponds to the mean SHAP value for that feature. Longer bars indicate a greater impact on the model's predictions
    
    **Ordering**: The bars (features) are sorted in descending order of their mean SHAP values
  ''')


# "SHAP Bar plots" section
st.space()
st.caption("Bar plots per profile")
shap_cols = st.columns(3, gap='medium', vertical_alignment='center')
profiles = ["Low Risk Profile", "Moderate Risk Profile", "High Risk Profile"]

assets_path= "assets/images/"
for i in range(len(shap_cols)):
  with shap_cols[i]:
    st.image(f"{assets_path}bar_plot_risk_profile_{i}.png", caption=profiles[i], output_format='PNG')   