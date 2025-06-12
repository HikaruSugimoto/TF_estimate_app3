import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from anndata import AnnData
import decoupler as dc
import seaborn as sns
import requests
import os
import zipfile
import gc
import base64

#Main
st.set_page_config(layout="wide")
st.title("TF activity inference")
#st.write("This website is free and open to all users and there is no login requirement.")

#1, upload omics data
#Slidebar
st.sidebar.subheader('1, Upload omics data')
TF_act_database= pd.read_csv("TF_act_data.csv")

if(os.path.isfile('demo.zip')):
    os.remove('demo.zip')
with zipfile.ZipFile('demo.zip', 'x') as csv_zip:
    csv_zip.writestr("demo.csv",
                    pd.read_csv("demo.csv").to_csv(index=False))    
with open("demo.zip", "rb") as file:
    #st.sidebar.download_button(label = "Download demo data",data = file,file_name = "demo.zip")
    zip_data = file.read()
    b64 = base64.b64encode(zip_data).decode()
    zip_filename = 'demo.zip'
    href = f'<a href="data:application/zip;base64,{b64}" download="{zip_filename}">Download demo data</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
if(os.path.isfile('demo.zip')):
    os.remove('demo.zip')
    
Tran = st.sidebar.file_uploader("Transcriptome data", type="csv")
if Tran is not None:
    st.subheader('Uploaded transcriptome data')
    Tran = pd.read_csv(Tran)
    st.write(Tran.set_index('index'))     
    
    tf_act,tf_p=dc.mt.ulm(data=Tran.set_index('index'),net=TF_act_database)
    st.write("TF activity")
    st.write(tf_act)

    st.write("TF adjusted pvalue")
    st.write(tf_p)

    if(os.path.isfile('TF_activity.zip')):
        os.remove('TF_activity.zip') 
    with zipfile.ZipFile('TF_activity.zip', 'x') as csv_zip:
        csv_zip.writestr("TF_activity.csv",
                        tf_act.to_csv(index=True))
        csv_zip.writestr("TF_adj_pvalue.csv",
                        tf_p.to_csv(index=True))               
    with open("TF_activity.zip", "rb") as file: 
        #st.download_button(label = "Download transporter data",data = file,file_name = "Transporter.zip")
        zip_data = file.read()
        b64 = base64.b64encode(zip_data).decode()
        zip_filename = 'TF_activity.zip'
        href = f'<a href="data:application/zip;base64,{b64}" download="{zip_filename}">Download the results</a>'
        st.markdown(href, unsafe_allow_html=True)
    if(os.path.isfile('TF_activity.zip')):
        os.remove('TF_activity.zip') 