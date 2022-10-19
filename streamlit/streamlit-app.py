# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 19:46:51 2022

@author: krish
"""

import pandas as pd
import streamlit as st
from elasticsearch import Elasticsearch
import configparser

config = configparser.ConfigParser()
config.read('example.ini')

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['username'], config['ELASTIC']['password'])
)

def img_search(ref_img):
    result = es.search(
        index = 'adm-assignment2',
        query = {
             "ids": {
                 "values": ref_img 
             }
        }
    )
    res_dict = result['hits']['hits'][0]['_source']
    return res_dict

def read_ref_imgs():
     return pd.read_csv('sim_index.csv')
 
def main():
    # Title embedded in html
    html_temp_title = """
            <div style="background-color:SteelBlue;padding:4px">
            <h1 style="color:white;text-align:center;">Visual Search for DeepFashion</h1>
            </div>
        """

    # Markdown
    st.markdown(html_temp_title, unsafe_allow_html=True)

    #Add sidebar to the app
    st.sidebar.markdown("##### Made by: :computer:")
    st.sidebar.markdown("### Aditi Krishna :dog:")
    
    # Get list of all images in the dataset
    images = read_ref_imgs()['ref_img']
    
    # Pick product image
    st.markdown("")
    st.markdown("")
    st.subheader("Select a product image from the list below: :point_down:")
    pic = st.selectbox('', images)
    img_path = 'all_imgs/'+pic
    st.image(img_path,width=None)
        
    # Slider to get number of similar items
    st.subheader("How many similar products would you like to see? :eyes:")
    n_sim = st.slider('', 1, 10, 5)
    # Subheading embedded in html
    html_temp_subhead = """
        <div style="background-color:#154360;padding:2px">
        <h2 style="color:White;text-align:center;">You May Also Like...</h2>
        </div>
    """
    # Markdown
    st.markdown(html_temp_subhead, unsafe_allow_html=True)
    st.markdown("")
    selected_img = img_search(pic)
    for img_count in range(len(selected_img)):
        if img_count < n_sim:
            img_name = list(selected_img.items())[img_count][1]
            path = 'all_imgs/' + img_name
            st.image(path, use_column_width=None, caption=img_name)
        
if __name__ == "__main__":
    main()
