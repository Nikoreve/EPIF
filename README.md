# Estimation and Personalised Interventions on elderly fallers (EPIF)

The project estimates the fall-risk profile a senior citizen is allocated to, based on his/her characteristics that are passed into a Machine Learning model. The data used to train the model, are based on the article of the citation.

<div align="center">
    <img src="assets/images/logo/epif_logo.jpg" width="700" height="300" alt="Logo">
</div>

## ℹ️ Overview

### 🌟 Usage
The project aims to contribute decision-making of a health proffesional in the field of falls. It provides personalized interventions based on the fall-risk profile and the features of the faller, in order to prevent future falls.

To use this application effectively, follow these steps:
1. Access the Online App [here](https://epifallers.streamlit.app)
2. Fill and Adjust Fields of the prediction section (Demographic, Medical, Physical Conditions, Functional, Phychological, Environmental)
3. Ackowledge the Fall-Risk Profile the elder is assigned to
4. View the Factors that impact the result the most
5. Get to know Personalized Interventions

### ✨ Highlights
• Estimates fall-risk profile on elderly people  
• Provides explainability based on local explanation  
• Offers personalised interventions based on senior's fall-risk profile and his/her characteristics  
• Includes useful material grasping the average trend of each fall-risk profile  
• Visualization of the most impactful factors for each fall-risk profile (based on shap global explanations)  
• Enriched glossary for each prediction field  
• Provision guidelines for each functional and phychological assessment (based on validated organizations in the field of falls)  
• FAQs  

### 📁 Dependencies
python==3.12  
streamlit==1.52.1  
matplotlib==3.10.8  
numpy==2.3.5  
pandas==2.3.3  
scipy==1.16.3  
seaborn==0.13.2  
shap==0.50.0  

## ⬇ Installation
> Prerequisites -> installed python v3.12
>
> 1. Clone this repo `git clone https://github.com/Nikoreve/EPIF.git`
>
> 2. Navigate to the folder the project has been installed into your computer
>
> 3. Create a Python virtual environment using venv module, run `python -m venv <env_name>` command
>
> 4. Activate it using `<env_name>/Scripts/Activate.ps1` (Windows) | `source <env_name>/bin/activate` (Linux/MacOS)
>
> 5. Run `pip install -r requirements.txt` to install the required dependencies.    
>
> 6. Launch the app by running `streamlit run Main.py`.    
>
> 7. 🎉 Open up your browser and navigate to *http://localhost:8501*  

## 🔖 Citation
```
@article{
title={Recording of Falls in Elderly Fallers in Northern Greece and Evaluation of Aging Health-Related Factors and Environmental Safety Associated with Falls: a Cross-Sectional Study},
authors={Lytras, Dimitrios and Sykaras, Evaggelos and Iakovidis, Paris and Kasimis, Konstantinos and Myrogiannis, Ioannis and Kottaras, Anastasios},
year={2022},
DOI={https://doi.org/10.1155/2022/9292673}, 
}
```
