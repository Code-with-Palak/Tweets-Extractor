
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

st.sidebar.markdown("<h1>Navigation!</h1>", unsafe_allow_html=True)
#selected_option = st.sidebar.radio("Select one-by-one",['Guide','Extract Tweets', 'Data', 'Visualization', 'Modelling', 'Performance'])
selected_option = st.sidebar.radio("Select one-by-one",['Extract Tweets', 'Data'])

if selected_option == "Extract Tweets":
    st.markdown("<h1 style='text-align: center; text-decoration: underline; color: Brown;'>Extract Tweets</h1>", unsafe_allow_html=True)
#     col1, col2 = st.columns(2)
#     img1 = Image.open(BASE_DIR+"elements/scrapping-tweets1.jpg")
#     img2 = Image.open(BASE_DIR+"elements/scraping-tweets.png")
#     img1 = img1.resize((1000,600))
#     img2 = img2.resize((1000,600))
#     col1.image(img1)
#     col2.image(img2)
    st.write("")
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

if selected_option == "Data":
    st.markdown("<h1 style='text-align: center; text-decoration: underline; color: Brown;'>Data Analytics</h1>", unsafe_allow_html=True)
    dataset=""
     
    if 'data' in st.session_state.keys():
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
        
    else:        
        upload_file = st.file_uploader("Choose a file")
        if upload_file is None:
            st.warning("Choose the data which is extracted from this app only!")
        if upload_file is not None:
            string_keywords = str(upload_file.name)
            st.session_state['string_keywords'] = string_keywords
            dataset = pd.read_csv(upload_file)
            if set(dataset.columns) == set(['UserName', 'Location', 'Text', 'Keyword']):
                dataset = dataset.sample(frac=1)
                dataset.reset_index(drop=True, inplace=True) 
                st.write("")
                st.write("")
                st.write("Complete dataset is shown here")
                st.write(dataset)
                st.session_state['data'] = dataset
            else:
                st.warning("Select the dataset retrived from this")
            
    if len(dataset)!=0:
        st.write("")
        st.write("")
        st.write("Description of the dataset")
        st.table(dataset.describe().T)
        st.write("Number of samples in the dataset: ",dataset.shape[0])
        st.write("Number of attributes in the dataset: ", dataset.shape[1])
        
