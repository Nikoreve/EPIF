import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sklearn
import streamlit as st
import helper.utils as ut
import helper.interventions as interv
import shap
import json

import time

logo_path = "./assets/images/logo/"

# Configurations
st.set_page_config(
  page_title = "EPIF",
  page_icon = f"{logo_path}epif_logo.jpg",
  layout = 'centered',
  menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': '''
        ### Estimation and Personalised Interventions on :blue[elderly] Fallers (EPIF)
        This application was developed by Nikolas Sarakenidis in the contenxt of his Master's thesis on Department of Information and Electronic Engineering at IHU, on fall-risk prediction and prevention in older adults. Supervisor professor of the project is Panagiotis Adamidis.
        
        Its purpose is to assist healthcare professionals, by providing a machine learning-based decision support tool for identifying fall-risk profiles and recommending personalized fall prevention interventions.
        '''
    })

# Deserializing serialized data
@st.cache_resource
def load_model():
  with open('./model/clf_pipeline.pkl', 'rb') as model_file:
    return pickle.load(model_file)

@st.cache_resource
def load_shap_explainer():
  with open('./model/shap_explainer.pkl', 'rb') as shap_explainer_file:
    return pickle.load(shap_explainer_file)
    
@st.cache_resource
def load_columns_types():
  with open('./data/columns_types.pkl', 'rb') as columns_types_file:
    return pickle.load(columns_types_file)

@st.cache_resource
def load_intervention_data():
  """ Return the intervention data """
  with open('./data/interventions.json', 'r', encoding="utf-8") as interventions_file:
    return json.load(interventions_file)


# https://docs.streamlit.io/develop/api-reference/widgets/st.number_input
# Get the value of the widget number_input
def functional_test_input(label, min, max, step, numeric_format, help_name):
  return st.number_input(
      label,
      min_value=min,
      max_value=max,
      step=step,
      format=numeric_format,
      help=help_name,
      key=label
  )


# Call serialazed data structures
model = load_model()

# -- Streamlit app --
header = st.container()

with header:
  st.markdown(
    "# Estimation and Personalised Interventions on :blue[elderly] Fallers <br> :older_woman: :older_man:",
    unsafe_allow_html=True,
    text_alignment='center'
  )
  st.space()

  # Description of the project
  st.markdown("""
              #### This application was developed as part of an undergraduate thesis for the Department of Information and Electronic Engineering at the International Hellenic University.
              """,
              unsafe_allow_html=True,
  )
  st.text(
    "Designed as an auxiliary tool for clinical practitioners, this application utilizes a Machine Learning model tailored for adults aged 65 to 80. The system focuses on individuals with a recent history of falls, categorizing them into specific classes (risk profiles) to suggest the most appropriate interventions. There are 3 distinct profiles.",
    text_alignment='justify'
  )
  st.text(
    "Certain input fields are subject to constraints due to the specific parameters of the dataset used to train the model.",
    text_alignment='justify'
  )
  st.space()


# Validation of each input field of the header section
# Returns the message of the error. If there is no error then return empty string
def input_validation(widget_names: list) -> str:
    non_prop_columns = numerical_columns + ordinal_columns + binary_columns
    prop_columns = [column for column in widget_names if column not in non_prop_columns]

    errors = []
    msg = ''
    # Checking if there is any 'key' that it doesn't exist in the widget_names list
    try:
      for key in non_prop_columns + prop_columns:
        if key in ('HospitalAdmissions', 'HospDays_min'): # The two features names are handled by an aggregated use, based on 'hospital_days_no' variable
          break
        if key not in st.session_state:
          errors.append(f"st.session_state has no key named '{key}'. ")
      if len(errors) != 0:
        raise ValueError(', '.join(errors))
    except ValueError as e:
      print(f'{e}\n\n Did you forget to initialize the key/s?')

    # Validating each input field value of prop fields
    fall_related_errors = []
    for i in range(1, falls_no + 1):
      fall_index_columns = [col for col in prop_columns if col.endswith(f"{i}")]
      # print('fall_index_columns', fall_index_columns)
      fall_index_labels_error = []
      for col in fall_index_columns:
        if type(col) in (int, float):
          # The column corresponds to a numeric input field which is already handled by the streamlit input field.
          break
        if st.session_state[col] is (None):
          # col name example : {label}_fall_{fall_index}'
          label, _, fall_index = col.split(sep='_')
          fall_index_labels_error.append(label)

      # Join every unfilled input into a list
      label_errors = ", ".join(f"'{x}'" for x in fall_index_labels_error)
      
      # Append error message
      if (len(fall_index_labels_error) == 1):
        errors.append(f"In fall case {i}, the {label_errors} field must be filled.")
      elif (len(fall_index_labels_error) > 0):
        errors.append(f"In fall case {i}, fields {label_errors} must be filled.")

  # Validating each input field value of binary fields
    fall_binary_input_error = []
    for col in binary_columns:
      if st.session_state[col] is (None):
        # col name example : has_{binary_feature}
        _, label = col.split(sep='_')
        fall_binary_input_error.append(label)
    
    # Join every unfilled input into a list
    binary_label_errors = ", ".join(f"'{x}'" for x in fall_binary_input_error)
    
    # Append error message
    if (len(fall_index_labels_error) == 1):
      errors.append(f"Field {binary_label_errors} must be filled.")
    elif (len(fall_index_labels_error) > 0):
      errors.append(f"Fields {binary_label_errors} must be filled.")

    # Format precisely the error message
    if errors: 
      # The list called 'errors' is not empty
      msg = f"You must fill every input field:\n\n {"  \n".join(errors)}"
    return msg


# Load features based on their types
numerical_columns, ordinal_columns, binary_columns, prop_columns = load_columns_types()

# Numerical columns
# general_purpose_columns = ['Age', 'Pills Per Day'] # , 'Hospital Admissions', 'Minimum Hospital Days'

# Binary columns
health_status_columns = ['Blood Test', 'Balance Deficitis', 'Cardiovascular Problems', 'Osteoporosis', 'Diabetes', 'Vertigo']

# Ordinal columns
activity_columns = {
  'PhysicalActivity': ['None', 'Walk', 'Intensive (i.e. Workout, Dance, Bike)']
}


# -- NON PREDICTION SECTION --

st.caption('The fields below, does not impact the model prediction')
general_info_cols = st.columns(2)

with general_info_cols[0]:
  falls_no = st.slider(
    'How many falls occured the last 12 months?',
    min_value=1,
    max_value=5,
    value=1,
    step=1,
    key='falls_no',
    help='Please select the number of fall incidents of the elder. The field affects the number of fall incident cases that will be drawn below'
  )

if(falls_no == 1):
  location_options = ['Indoor', 'Outdoor']
else:
  location_options = ['Indoor', 'Outdoor', 'Both']

with general_info_cols[1]:
  fall_location = st.selectbox(
    label='Fall location',
    options=location_options,
    # default='Inside',
    index=0,
    key='fall_location',
    width='stretch',
    help='The field is used to inform appropriate personalised interventions'
  )


# -- PREDICTION section --

CATEGORICAL_PROPORTIONAL_WEIGHT = 0.2 # The weight of the proportional features of the dataset

st.space(size="medium")
with st.form("model_fields_form", border=False):
  st.header('Predict patient profile')
  st.divider()

  # model[0] -> StandardScaler
  # model[1] -> SVC model
  user_inputs = {k:None for k in model[0].get_feature_names_out()}
  # print(user_inputs)

  st.caption('Demographic')
  user_inputs['Age'] = st.number_input(
    label='Age',
    min_value=65,
    max_value=80,
    step=1,
    key='Age')

  st.space()
  st.caption('Health Status')
  
  user_inputs['PillsPerDay'] = st.slider(
    label='Pills Per Day',
    min_value=0,
    max_value=5,
    step=1,
    key='PillsPerDay')

  clinical_cols = st.columns(2)
  for i, (col, model_col) in enumerate(zip(health_status_columns, binary_columns)):
    target_col = 0 if i%2==0 else 1
    if 'Blood Test' in col:
      placehldr = f'Does the faller have regular blood check-ups?'
    else:
      placehldr = f'Does the faller have {col}?'
    with clinical_cols[target_col]:
      selected = st.selectbox(
        label=col,
        placeholder=placehldr,
        options=['No', 'Yes'],     
        index=None,
        key=model_col)
      user_inputs[model_col] = 1 if selected == 'Yes' else 0

  phys_activ_selected = st.selectbox(
    label='Physical Activity',
    options=activity_columns['PhysicalActivity'],
    index=0,
    key='PhysicalActivity')
  user_inputs['PhysicalActivity'] = activity_columns['PhysicalActivity'].index(phys_activ_selected) + 1 # Increment by 1 because: the values of the corresponding feature are in the form of: 1,2,3

  st.space()
  st.caption('Functional Tests')
  
  idx = 0
  functional_test_item = []
  functional_cols = st.columns(2)
  while(idx < len(ut.functional_test_data['column'])):
    if(ut.functional_test_data['type'][idx] in ['int', 'float']):
      for col in ut.functional_test_data:
        if(col != 'type'):
          functional_test_item.append(ut.functional_test_data[col][idx])
      target_col = 0 if idx%2==0 else 1
      with functional_cols[target_col]:
        user_inputs[ut.functional_test_data['column'][idx]] = functional_test_input(*functional_test_item)
    else:
      raise TypeError("Only integers and floats are allowed (as 'type' value).")
    functional_test_item.clear()
    idx += 1

  st.space()
  st.caption('Fall Related')

  # CARDS - per fall incident
  if "cards" not in st.session_state:
    st.session_state.cards = {}
      
  fall_index = 0
  hospital_days_no = []

  # Return all proportioned (prior categorical) features
  all_categorical_features = [option for sublist in ut.prop_columns.values() for option in sublist]
  
  # Return a dict containing: k: proportioned feature name, v: numerical value
  input_prop_data = {feature: 0.0 for feature in all_categorical_features}
  # print(input_prop_data.keys())

  widgets_key_names = []
  widgets_key_names.extend(ut.widgets_key_names)
  # print('before: ', widgets_key_names)

  # Creates a card for each fall case
  # Returns the current index of which is called {fall_index}
  def card_column(fall_index):
    # The keys of widgets inside the card, has the form: hosp_days_fall_{fall_index}. They are not in the form of the model's features names
    fall_index += 1
    st.write(f'Fall Case {fall_index}')
    
    key_name = f'hosp_days_fall_{fall_index}'
    if key_name not in widgets_key_names:
        widgets_key_names.append(key_name)
    
    days = st.number_input(
      label='Days of hospitalization',
      min_value=0,
      max_value=20,
      label_visibility='visible',
      help='The limit value is 20, due to the need of consistency with the data the model had fit to.',
      step=1,
      key=key_name
    )
    hospital_days_no.append(days)

    for label, options in ut.prop_columns.items():
      key_name = f'{label}_fall_{fall_index}'
      if key_name not in widgets_key_names:
        widgets_key_names.append(key_name)
        
      selected = st.selectbox(
        label=f'Select fall {label}',
        options=options,
        index=None,
        # help='Need help?',
        key=key_name
      )
      if selected and selected in input_prop_data:
        input_prop_data[selected] += CATEGORICAL_PROPORTIONAL_WEIGHT
        if(selected != 'Other'): 
          # There is no feature called 'Other'. It's just for convenience of user
          real_feature_name = ut.prop_columns_mapping[selected]
          user_inputs[real_feature_name] = input_prop_data[selected]
    return fall_index

  # Dynamic Fall cards creation
  for i in range(0, falls_no, 2):
    if(fall_index+2 > falls_no):
      col = st.container(border=True)
      with col:
        fall_index = card_column(fall_index)
    else:
      cols = st.columns(2, gap="medium", border=True)

      # left CARD
      with cols[0]:
        fall_index = card_column(fall_index)
      
      # right CARD
      with cols[1]:
        fall_index = card_column(fall_index)


  user_inputs['HospDays_min'] = min(hospital_days_no)
  user_inputs['HospitalAdmissions'] = sum(x>0 for x in hospital_days_no)

  try:
    # The 'else 0.0' statement is very suspicious and prone to make the debuggind difficult
    # It may change in the future

    # round the numerical features values into 2 decimals
    user_inputs = {k: round(v, 2) if(isinstance(v,(int, float))) else 0.0 for k, v in user_inputs.items()}
  except:
    raise Exception('An error occured when user_inputs converted to round. Maybe incorrect |user_input| type.')

  submit_button = st.form_submit_button(label='Predict profile', key='form_submit_button')

  st.space(size="small")


  def check_close_classes(winner_prob, probs):
    threshold = 0.10
    print('probs:', probs)
    close_classes = [ c for c, p in enumerate(probs) if ((winner_prob - p) <= threshold) ]
    return close_classes
    
  
  if submit_button:
    # st.session_state.form_submit_button = True
    msg = input_validation(widgets_key_names)

    input_row_df = pd.DataFrame([user_inputs])#, columns=user_inputs.keys())

    if len(msg) == 0:
      try:
        # Predict
        y_pred_proba = model.predict_proba(input_row_df)
        # print('y_pred_proba: \n',y_pred_proba)
        
        winner_class = np.argmax(y_pred_proba)
        # print('y_pred_proba[winner_class]: ', y_pred_proba[0][winner_class])
        # print('winner_class: ', winner_class)
        
        close_classes = check_close_classes(y_pred_proba[0][winner_class], y_pred_proba[0])
        # print('close_classes are:', close_classes)
        
        y_pred_proba_df = pd.DataFrame(y_pred_proba)
        y_pred_proba_df.columns = ["Low risk", "Moderate risk", "High risk"]

        
        st.space()
        st.subheader('Predicted Profile')
        # Show DataFrame
        st.dataframe(y_pred_proba_df, hide_index=True,
                    column_config={
              "Low risk": st.column_config.ProgressColumn(
              label="Low risk",
              format="%.3f",
              min_value=0,
              max_value=1
            ),
              "Moderate risk": st.column_config.ProgressColumn(
              label="Moderate risk",
              format="%.3f",
              min_value=0,
              max_value=1
            ),
              "High risk": st.column_config.ProgressColumn(
              label="High risk",
              format="%.3f",
              min_value=0,
              max_value=1
            )
          })

        # Success message
        st.success(f'The patient was successfully assigned to: {y_pred_proba_df.columns[winner_class].upper()} profile', icon=":material/done:", width="stretch")

        # -- Interpertation section --
        st.space(size="small")
        st.subheader("Why was the patient assigned to this profile?")
        st.markdown(f"Based on the baseline of {y_pred_proba_df.columns[winner_class]} profile, the features that pushed the result into it are shown in red, opposing featues are shown in blue: ")

        # Interpretation of results using SHAP library
        explainer = load_shap_explainer()
        shap_values = explainer(input_row_df)
        # shap_values.shape
        
        waterfall_cols = st.columns(len(close_classes))
        i = 0
        for class_id in close_classes:
          with waterfall_cols[i]:
            print(winner_class, ':', class_id)
            if (class_id == winner_class):
              st.markdown(f":green-badge[:material/check: {y_pred_proba_df.columns[class_id]}]", text_alignment = "center")
            else:
              st.markdown(f":gray-badge[:material/clear: {y_pred_proba_df.columns[class_id]}]", text_alignment = "center")
            plt.figure(figsize=(6, 5))
            plot = shap.plots.waterfall(
              shap_values[0, :, class_id],
              # shap_values[0, :, winner_class],
              max_display=10
            )
            st.pyplot(plt.gcf())
  
          # Clear figure to avoid overlaps
            plt.clf() 
            i += 1

        # -- Interventions section --
        st.space()
        class_key = f"class_{winner_class}"
        interv_data = load_intervention_data()
        location_type = st.session_state.fall_location
        # print("render_interventions parameters:",  class_key, "|", location_type, "|", "Time: ", time.localtime(time.time()))

        # Get intervention data 
        class_data = interv_data.get(class_key)

        # Call intervention display function
        interv.render_interventions(class_data, location_type)
        
      except Exception as e:
        print(e, 'L0000L')
    else:
      st.error(msg, icon='🚨')