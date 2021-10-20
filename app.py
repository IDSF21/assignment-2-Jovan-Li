 
import pickle
import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
 
# loading the trained model
pickle_in = open('classifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)
clean_data = pd.read_csv("Cleaned_Satisfaction.csv")
 
@st.cache()
  
# defining the function that will make the prediction using the data the user inputs 
def prediction(Cus_Type, Class, Flight_Dist, Seat_Comfort, In_Wifi_Ser, 
            In_Enter, Cleanliness, Depart_Delay, Arrival_Delay):   
 
    # Pre-processing user input    
    if Cus_Type == "Loyal Customer":
        Cus_Type = 1
    else:
        Cus_Type = 0
 
    if Class == "Business":
        Class = 2
    elif Class == "Eco Plus":
        Class = 1
    else:
        Class = 0
    
    if Seat_Comfort == "Very Comfortable":
        Seat_Comfort = 5
    elif Seat_Comfort == "Comfortable":
        Seat_Comfort = 4
    elif Seat_Comfort == "Ordinary":
        Seat_Comfort = 3
    elif Seat_Comfort == "Uncomfortable":
        Seat_Comfort = 2
    elif Seat_Comfort == "Very Uncomfortable":
        Seat_Comfort = 1
    else:
        Seat_Comfort = 0
    
    if In_Wifi_Ser == "Excellent":
        In_Wifi_Ser = 5
    elif In_Wifi_Ser == "Good":
        In_Wifi_Ser = 4
    elif In_Wifi_Ser == "Ordinary":
        In_Wifi_Ser = 3
    elif In_Wifi_Ser == "Unstable":
        In_Wifi_Ser = 2
    elif In_Wifi_Ser == "Poor":
        In_Wifi_Ser = 1
    else:
        In_Wifi_Ser = 0
    
    if In_Enter == "Excellent":
        In_Enter = 5
    elif In_Enter == "Good":
        In_Enter = 4
    elif In_Enter == "Ordinary":
        In_Enter = 3
    elif In_Enter == "Poor":
        In_Enter = 2
    elif In_Enter == "Disappointing":
        In_Enter = 1
    else:
        In_Enter = 0
        
    if Cleanliness == "Excellent":
        Cleanliness = 5
    elif Cleanliness == "Good":
        Cleanliness = 4
    elif Cleanliness == "Ordinary":
        Cleanliness = 3
    elif Cleanliness == "Poor":
        Cleanliness = 2
    elif Cleanliness == "Messy":
        Cleanliness = 1
    else:
        Cleanliness = 0
    
 
    # Making predictions 
    prediction = classifier.predict( 
        [[Cus_Type, Class, Flight_Dist, Seat_Comfort, In_Wifi_Ser, 
            In_Enter, Cleanliness, Depart_Delay, Arrival_Delay]])
     
    if prediction == 0:
        pred = 'Neutral or Dissatisfied'
    else:
        pred = 'Satisfied'
        
    return pred

def short_score(value):
    return '{0:.3f}'.format(value)
   
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:blue;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Airflight Satisfaction Prediction</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
    
    #first let's find out every user's average ratings for the flight
    clean_data['Rating Average'] = clean_data[['Seat Comfort','Inflight Wifi Service',
                                               'Inflight Entertainment','Cleanliness']].mean(axis = 1)
    
    st.header("1. Let's first explore the relationship between some features and satisfaction")
    
    st.subheader('The relationship between Flight Distance and Class')
    fig, ax = plt.subplots(figsize=(6,6))
    ax = sns.histplot(x='Flight Distance', hue='Class', data=clean_data, kde=True, palette='viridis')
    average = np.average(clean_data['Flight Distance'])
    plt.axvline(average, color='red')
    plt.legend(labels=[*['Business','Eco Plus', 'Eco'], f'Average ({short_score(average)})'], loc='center left', bbox_to_anchor=(1, 0.5))
    st.pyplot(fig)
    
    
    st.subheader('Passenger Average Rating Distribution')
    clean_data['Rating Average'] = clean_data['Rating Average'].astype(int)
    fig, ax = plt.subplots(figsize=(6,6))
    ax = sns.countplot(x='Rating Average', data=clean_data, palette='viridis')
    st.pyplot(fig)
    
    st.subheader('Correlation between Features')
    fig, ax = plt.subplots(figsize=(6,6))
    ax = sns.heatmap(clean_data.corr(), annot = True, vmin=-1, vmax=1, center= 0, 
                     fmt = '.1f', cmap=plt.cm.viridis, linecolor='white', linewidths=0.9)
    st.pyplot(fig)
    
    
    st.header("2. Let's use these features to make a prediction!")
    # following lines create boxes in which user can enter data required to make prediction 
    Cus_Type = st.selectbox('Customer Type',("Loyal Customer", "Others"))
    
    Class = st.selectbox('Travel Class', ("Business", "Eco Plus", "Eco")) 
    
    Flight_Dist = st.slider('Flight Distance', 100, 3500)
    
    Depart_Delay = st.slider('Departure Delay in Minutes', 0, 150)
    
    Arrival_Delay = st.slider('Arrival Delay in Minutes', 0, 150)
    
    Seat_Comfort = st.selectbox('Seat Comfortness', ("Very Comfortable", "Comfortable", 
                                                     "Ordinary", "Uncomfortable", "Very Uncomfortable",
                                                    "Painful"))
    
    In_Wifi_Ser = st.selectbox('Inflight Wifi Service',("Excellent", "Good", "Ordinary",
                                                "Unstable", "Poor", "No Service"))
    
    In_Enter = st.selectbox('Inflight Entertainment',("Excellent", "Good", "Ordinary",
                                                "Poor", "Disappointing", "No Entertainment"))
    
    Cleanliness = st.selectbox('Cleanliness',("Excellent", "Good", "Ordinary",
                                                "Poor", "Messy", "Disgusting"))
    
    result =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(Cus_Type, Class, Flight_Dist, Seat_Comfort, In_Wifi_Ser, 
                            In_Enter, Cleanliness, Depart_Delay, Arrival_Delay) 
        st.success('The passenger is {} with this air travel'.format(result))
     
if __name__=='__main__': 
    main()
