
import sys, re
import pandas as pd
BASE_DIR = 'https://github.com/Code-with-Palak/Tweets-Extractor/tree/main/'
vis_dirct = 'https://github.com/Code-with-Palak/Tweets-Extractor/tree/main/visualization/'
sys.path.append(BASE_DIR)
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from tweetsExtract import tweet_extractor, convert_df


st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown("<h1 style='text-align: center; text-decoration: underline; color: White;'>Extract Tweets</h1>", unsafe_allow_html=True)
string_keywords = st.text_input("Enter your keywords coma(,) seperated")#, placeholder="Enter keyword(s)"
keywords = string_keywords.split(',')

for i in range(len(keywords)):
    keywords[i] = re.sub(' ','',keywords[i])
col1, col2 = st.columns(2)
date = col1.date_input('Select starting date')
n_tweets = col2.number_input('Number of tweets', step=10)
st.session_state['string_keywords'] = string_keywords
st.write("")
st.write("")
click = st.button("Extract Tweets")
if click:
    if string_keywords and n_tweets:
        # try:
            if len(keywords)>0 and date and n_tweets:
                with st.spinner("Fetching..."):
                    dataset = tweet_extractor(keywords, date, n_tweets=n_tweets)
                st.session_state['data'] = dataset
                st.success("Data has been fetched from the twitter, successfully!")
                
        # except:
        #     st.warning("Check your connection and refresh!")
    else:
        st.warning("Enter the 'complete' data!")



dataset=""
    
if 'data' in st.session_state.keys():
    st.markdown("<h1 style='text-align: center; text-decoration: underline; color: White;'>Dataset</h1>", unsafe_allow_html=True)
    dataset = st.session_state['data']
    st.write(dataset)        
    
    csv = convert_df(dataset)
    string_keywords = st.session_state['string_keywords']
    d = st.download_button(
        label="Download Data",
        data=csv,
        file_name=f'data({string_keywords})).csv')
    if d:
        st.success(f"Data is downloaded for the keyword: {string_keywords}")
        
