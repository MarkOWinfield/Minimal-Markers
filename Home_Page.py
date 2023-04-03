#!/usr/bin/env python

"""
    This script is based on the latest, modified verion of the distance_matrix.py
    script (resolves the problem of using '9', no score, in comparisons of 
    distance).  However, this modified version of the script accepts a 
    snp-profile as input (this could be a single input or from a file
    over which it has to loop) and looks for identical snp-profiles, or 
    compatible because of 9s, from the database file and outputs a list of these.
    It writes the lists of these to a separate files.   
    
    Mark Winfield 13/06/22.

"""

from __future__ import division

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

  

st.markdown("""
            # Minimal Marker Page
            ### Based on data apple and wheat datasets
            
            ---
            
            """
            )


col1, col2 = st.columns([2,1], gap='large')

with col1:
    
    st.markdown("""
            
            This simple APP has been created to make it possible to upload files
            containing minimal marker based SNP profiles of unidentified wheat
            and apple varieties and compare them against databases containing
            significant numbers of named varieties that have been genotyped by
            the genomics group at The University of Bristol.
            
            Specifically, the wheat database contains minimal marker, SNP profiles
            of 2,490 accessions (including 835 Watkins lines), and the apple database
            contains profiles of over 1800 apple varieties, both desert and cider,
            obtained from the National Fruit Collection at Brogdales in Kent.
            
            """
            )
        
    st.image('./images/wheat_and_apple_query_header.png', 'Example csv files containing SNP profile for wheat and apple')
    
    st.markdown("""
                
            To begin uploading your files, select the relevant database, wheat
            or apple, from the sidebar menu on the left.
            
            """
            )    
    
with col2:
    
    st.image('./images/wheat_and_apple_small.png')
  
    
st.markdown('---')