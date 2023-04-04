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

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.DataFrame(columns = ['Query_sample', 'Match_in_Database', 'Number_of_Matching_Markers', 'Number_of_9s', 'Number_of_Differences'])

  
############################### FUNCTIONS #####################################

@st.cache_data
def getData():
    dfAppleRef = pd.read_csv('./data/apple_lookup_table.csv')

    return dfAppleRef


def dist(var1, ref_profile, query_profile):

    diffs = 0
    sames = 0
    nines = 0
    total = 0
    
    for i in range(0, len(ref_profile)):

        if query_profile[i] == '9' or ref_profile[i] == '9':
            nines = nines + 1
            diffs = diffs
            sames = sames
        elif query_profile[i] == ref_profile[i]:
            sames = sames + 1
        elif query_profile[i] != ref_profile[i]:
            diffs = diffs + 1

    total = diffs + sames
   
    return diffs, sames, nines, total;


@st.cache_data
def convert_df(df):

    return df.to_csv().encode('utf-8')

###############################################################################


st.markdown("""
            # Apple Minimal Markers
            ### Query the SNP profile database
            
            ---
            
            """
            )


col1, col2, col3 = st.columns(3, gap='large')

with col1:
    
    st.image('./images/Brogdale_04MOD.jpg', caption = 'Apple from Brogdales')
    
    
with col2:
    
    st.markdown("""
            
            Upload a csv containing the SNP profiles of the apple accessions 
            you wish to compare against the Brogdale database.  The csv file
            should contain two columns; the first column, header 'Sample' contains
            the name of the sample; the second column, header 'Profile' contains
            the profile which should be a a 21 character string containing only
            the numbers 0, 1, 2 and 9:
            
            """
            )
        
    st.image('./images/apple_query_header.png')

    st.markdown("""
            
            Once a file has been uploaded, a 'Results' section will appear below.
            The results table may be downloaded as a CSV file.
            
            The underlying database against which the query profiles are being
            compared may also be visualised, should you wish, by checking the
            box labelled 'Show apple SNP database'.
            
            """
            )

with col3:
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:

        # Can be used wherever a "file-like" object is accepted:
        dfQuery = pd.read_csv(uploaded_file)
        if st.checkbox('Show uploaded file', key = 1):
            st.write(dfQuery)    
    

    allowed_fails = st.selectbox(
        'How many failed markers do you wish to allow?',
        [0, 1, 2, 3, 4, 5], 2, key = 2)

    
    allowed_mismatches = st.selectbox(
        'How many mismatches do you wish to allow?',
        [0, 1, 2, 3], key = 3)

     
st.markdown('---')

if uploaded_file is not None:
        
    dfAppleRef = getData()
        
    st.subheader('Results')

    for index, row in dfQuery.iterrows():
        sample = row['Sample']
        query_profile = row['Profile']
        var_list = []
        query_profile = list(query_profile)
        counter = 0
        
        for index, row in dfAppleRef.iterrows():
            counter += 1
            var1 = row['Accession Name']
            ref_profile = row['Profile']
            ref_profile = list(ref_profile)
            
            diffs, sames, nines, total = dist(var1, ref_profile, query_profile)
    
      # Adds accessions with the same SNP profile as the query to a list.
      # If one wished, one could set the distance to be higher than 0  
      # thus permitting an error rate in scoring to be taken into account.
      # For example, one error in 21 markers would result in a  
      # distance of 0.0476; so could use 'if distance <= 0.05'
      # I have also added a lower limit to the number of comparisons that need
      # to be called so that distance isn't based on only one or two SNPs.
          
            if diffs <= allowed_mismatches and total >= 21 - allowed_fails:
                var1 = var1 + ', ' + str(sames) + ', ' + str(nines) + ', ' + str(diffs)
                var_list.append(var1)

        if len(var_list) >= 1:

            for var in var_list:
                        #st.write(var)
                var_split = var.split(', ')
                
                df.loc[len(df)] = {'Query_sample': sample, 'Match_in_Database': var_split[0],
                                  'Number_of_Matching_Markers': var_split[1],
                                  'Number_of_9s': var_split[2],
                                  'Number_of_Differences': var_split[3]}
 
        else:
 
            count_nines = query_profile.count('9')

            df.loc[len(df)] = {'Query_sample': sample, 'Match_in_Database': 'NO SIMILARITIES',
                               'Number_of_Matching_Markers': 'NA',
                               'Number_of_9s': str(count_nines),
                               'Number_of_Differences': 'NA'}                 
  
        # Remove duplicates based on the 'Query_sample' column.  This is because
        # there are still duplicates in the 'apple_lookup_table.csv' although
        # these are likely to be synonyms.  One only wants to count and plot a
        # single variety for each of the input profiles. 
        # NB One might not want to delete duplicates when one is searching with
        # mismatches allowed.
        
    df.drop_duplicates(subset='Query_sample', keep='last', inplace=True)

# From the dataframe, 'df', created above,  count the number of occurences of
# each of the matched varieties 
#       NO SIMILARITIES           29
#       Aldenham Blenheim          5
#       Coxs Orange Pippin 1       4
#       Crimson Bramley            2
#       Grenadier 1                2
#       Harry Masters Jersey 2     2
#       Browns Apple 1             1
#       Scarlet Pimpernel          1
#
# and covert it to a new dataframe, 'df_final_counts'.

if uploaded_file is not None:
    
    col1, col2 = st.columns([1,2], gap='large')
    
    with col1:

        df_final_counts = df.Match_in_Database.value_counts().reset_index()
        df_final_counts.columns = ["Match", "Number"]
        df_final_counts.rename(index=df_final_counts.Match, inplace=True)
        df_final_counts.sort_values(by='Number', ascending=False, inplace=True)
        st.write(df_final_counts)

    with col2:
 
        fig = px.pie(df_final_counts, values='Number', names='Match', title='Varieties Found')
        st.plotly_chart(fig)

csv = convert_df(df)

st.download_button(
    "Press to Download",
    csv,
    "matches_to_apple_database.csv",
    "text/csv",
    key='matches_to_database'
    )
