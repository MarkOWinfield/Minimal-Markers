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

  
############################### FUNCTIONS #####################################


# @st.cache(suppress_st_warning=True)
# def getData(filePath):
#     dfRef = pd.read_csv(filePath)
     
#     return dfRef


def dist(var1, ref_profile, query_profile):

    diffs = 0
    sames = 0
    distance = []
    total = 0
    
    for i in range(0, len(ref_profile)):

        if query_profile[i] == '9' or ref_profile[i] == '9':
            diffs = diffs
            sames = sames
        elif query_profile[i] == ref_profile[i]:
            sames = sames + 1
        elif query_profile[i] != ref_profile[i]:
            diffs = diffs + 1

    total = diffs + sames
   
    if diffs >= 1:
        if diffs == total:
            distance = 1
        else:
            distance = diffs / total
    elif diffs == 0:
        distance = 0

    return diffs, distance, total;


###############################################################################


st.markdown("""
            # Wheat Minimal Markers
            ### Query the SNP profile database
            
            ---
            
            """
            )


col1, col2, col3 = st.columns(3, gap='large')

with col1:
    
    st.image('./images/wheat.jpg', caption = 'Wheat ears')
    
    
with col2:
    
    st.markdown("""
            
            Upload a csv containing the SNP profiles of the wheat accessions 
            you wish to compare against the CerealsDB database.  The csv file
            should contain two columns; the first column, header 'Sample' contains
            the name of the sample; the second column, header 'Profile' contains
            the profile which should be a a 32 character string containing only
            the numbers 0, 1, 2 and 9:
            
            """
            )
        
    st.image('./images/wheat_query_header.png')
            

with col3:

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:

        # Can be used wherever a "file-like" object is accepted:
        dfQuery = pd.read_csv(uploaded_file)
        if st.checkbox('Show uploaded file', key = 1):
            st.write(dfQuery)    
    
    
st.markdown('---')

col1, col2 = st.columns([1,2], gap='large')

with col2:
    
    dfWheatRef = pd.read_csv('./data/wheat_lookup_table.csv')

    if st.checkbox('Show wheat SNP profile database', key = 2):

        st.write(dfWheatRef)

with col1:
    
    st.subheader('Results')

    if uploaded_file is not None:

        if st.checkbox('Check the box to see the results', key = 3):
            # Iterate all rows using DataFrame.iterrows()
            for index, row in dfQuery.iterrows():
                sample = row['Sample']
                query_profile = row['Profile']
        
                allowed_fails = 4
                allowed_diffs = 1
    
                var_list = []
                query_profile = list(query_profile)
                counter = 0
        
                for index, row in dfWheatRef.iterrows():
                    counter += 1
                    var1 = row['Accession']
                    ref_profile = row['Profile']
                    ref_profile = list(ref_profile)
            
                    diffs, distance, total = dist(var1, ref_profile, query_profile)
    
          # Adds accessions with the same SNP profile as the query to a list.
          # If one wished, one could set the distance to be higher than 0  
          # thus permitting an error rate in scoring to be taken into account.
          # For example, one error in 21 markers would result in a  
          # distance of 0.0476; so could use 'if distance <= 0.05'
          # I have also added a lower limit to the number of comparisons that need
          # to be called so that distance isn't based on only one or two SNPs.
          
                    if diffs <= allowed_diffs and total >= 21 - allowed_fails:
                        var1 = var1 + ',' + str(total)
                        var_list.append(var1)


#    text_to_write = '<p style="font-family:sans-serif; color:Green; font-size: 32px;">Query sample,</p>'
   
                if len(var_list) >= 1:
#        st.markdown(text_to_write, unsafe_allow_html=True)
                    st.subheader(f'Query sample: {sample}')
                    for var in var_list:
                        st.write(var)
                    st.markdown('---')

                else:
                    st.subheader(f'Query Sample: {sample}')
                    st.write('NO SIMILARITIES\n')
                    st.markdown('---')