# Widgets info
functional_test_data = {
  'column': ['BBS_Score', 'FICSIT4_Score', 'ShortFESI_Score', 'TUG_Score'],
  'type': ['int','int','int','float'],
  'min': [0, 0, 7, 3.0], # the last has been assigned as 3.0 arbitrarly, as there none can achieve in less seconds the test
  'max': [56, 28, 28, 15.0],
  'step': [1, 1, 1, 0.1],
  'format': [None, None, None, "%0.2f"],
  'help_name': [
    "Berg Balance Scale. For more information check page 'Glossary'",
    "Frailty and Injuries: Cooperative Studies of Intervention Techniques (FICSIT-4). For more information check page 'Glossary'",
    "Short Falls Efficacy Scale International (Short FES-I) Score Questionnaire. For more information check page 'Glossary'",
    "Timed Up-and-Go. The unit is in seconds (s). For more information check page 'Glossary'"
  ]
}

# Proportioned columns info
prop_columns = {
  'Cause': [
    'Tripped on Something',
    'Lost balance while sitting up or down',
    'Dizziness',
    'Trying to reach something high',
    'Other'
  ],
  'Location': [
    'Bedroom',
    'Bathroom',
    'Stairs (either at home or out)',
    'Yard or Balcony',
    'Pavement or Road',
    'Other'
  ],
  # 'Part of the day'
  'Time': [
    'Morning',
    'During the day',
    'Night (before bedtime)',
    'Night (at bedtime)'
  ] 
}

prop_columns_mapping = {
     'Tripped on Something': 'FallCause_TrippedOnSomething',
     'Lost balance while sitting up or down': 'FallCause_UpDownSitting',
     'Dizziness': 'FallCause_Dizzines',
     'Trying to reach something high': 'FallCause_ReachingHighObject',
     'Bedroom': 'FallSiteMerged_Bedroom',
     'Bathroom': 'FallSiteMerged_Bathroom',
     'Stairs (either at home or out)': 'FallSiteMerged_Stairs',
     'Yard or Balcony': 'FallSiteMerged_YardBalcony',
     'Pavement or Road': 'FallSiteMerged_PavementRoad',
     'Morning': 'FallTime_InMorning',
     'During the day': 'FallTime_DuringDay',
     'Night (before bedtime)': 'FallTime_NightBeforeBed',
     'Night (at bedtime)': 'FallTime_NightAtBed',
}

widgets_key_names = [
 'Age',
 'BBS_Score',
 'has_BloodTest',
 'has_BalanceDeficitis',
 'has_CardiovascularProblems',
 'FICSIT4_Score',
 # 'FallCause_TrippedOnSomething',
 # 'FallCause_UpDownSitting',
 # 'FallCause_Dizzines',
 # 'FallCause_ReachingHighObject',
 # 'FallSiteMerged_Bedroom',
 # 'FallSiteMerged_Bathroom',
 # 'FallSiteMerged_Stairs',
 # 'FallSiteMerged_YardBalcony',
 # 'FallSiteMerged_PavementRoad',
 # 'FallTime_InMorning',
 # 'FallTime_DuringDay',
 # 'FallTime_NightBeforeBed',
 # 'FallTime_NightAtBed',
 # 'HospitalAdmissions',
 # 'HospDays_min',
 'has_Osteoporosis',
 'PillsPerDay',
 'PhysicalActivity',
 'ShortFESI_Score',
 'TUG_Score',
 'has_Diabetes',
 'has_Vertigo',
 ]