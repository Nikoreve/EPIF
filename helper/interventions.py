import streamlit as st

def render_interventions(class_data, location_type):
  """ Returns the UI interventions for the specified elder.

  Keyword argument:
  class_data    -- intervention data for the specified elder
  location_type -- The location type of elder's fall/s (possible values: "indoor", "outdoor", "both")
  """

  # Check if class_data exist
  if not class_data:
      st.warning("No interventions found for this profile.")
      return

  # `Interventions` section
  st.subheader(f"Individualized interventions")
  st.badge(f"based on {class_data["title"]}")
  st.space()

  # Description of class
  if "description" in class_data:
      st.write(class_data["description"])

  # Text of focused areas of the class
  if "focus" in class_data:
      with st.expander("🎯 Focus ", expanded=True):
          for f in class_data["focus"]:
              st.markdown(f"• {f}")

  
  st.space()
  st.caption("🛠 Recommended Interventions")

  # Rule-based filter of the location type of fall/s of elder
  blocked_intervention = ""
  match location_type:
    case "Indoor":
      blocked_intervention = "outdoor_interventions"
    case "Outdoor":
      blocked_intervention = "indoor_interventions"
    case "Both":
      blocked_intervention = ""

  # Recommendations-Interventions based on: (a) class and (b) personalized fall/s conditions
  for section in class_data["interventions"]:
    if (section["code"] == blocked_intervention):
      continue
    with st.expander(section["title"], expanded=True):
      for item in section["items"]:
        st.markdown(f"• {item}")