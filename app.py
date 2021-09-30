import numpy as np
import pickle
import pandas as pd
import streamlit as st
import clean
import base64
from PIL import Image

def main():
    st.set_page_config(layout= "wide")

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        st.write("")

    # with col2:
    #     st.sidebar.image('Compunnel-Digital-Logo.png',width=125)

    with col3:
        st.write("")

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")

    st.title('''**Succession Planner**''')
    st.subheader("This platform helps you to find the right Talent!")
    st.write("    ")
    st.write("    ")
    
    uploaded_files= st.sidebar.file_uploader("Upload Resume",type=['docx'],accept_multiple_files=True)
    file_lst = [uploaded_file.name for uploaded_file in uploaded_files]
    jd_files = st.sidebar.file_uploader("Upload Job Description",type=['docx'],accept_multiple_files=True)
    jd_lst = [jd.name for jd in jd_files]
    # query= st.sidebar.text_input("Enter The Query:")

    if st.sidebar.button("Match"):
        df = pd.DataFrame(columns=['Job_Description','Resume','Score','Top_Keywords','Next Steps'])
        result_jd = clean.cleanData(clean.getText(jd_lst[0]))
        
        for eachResume in file_lst:
            result_rc = clean.cleanData(clean.getText(eachResume))
            record = [result_rc, result_jd]
            response = clean.howmuchsimilar(record)
            nextRound = clean.thresholddata(response[0])
            df.loc[len(df.index)] = [record[1][:100]+"...",record[0][:100]+"...",response[0],response[1],nextRound]

        st.info("Recommended candidates")
        df_new = df.sort_values(by=['Score'], ascending=False)
        st.write(df_new.to_html(escape=False, index=False), unsafe_allow_html=True)
    

if __name__=='__main__':
    main()
