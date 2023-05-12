import webbrowser
import streamlit as st
import pandas as pd
import numpy as np 
from math import pi
import matplotlib.pyplot as plt
#import plotly.express as px


def wide(): 
    st.set_page_config(layout="wide")
wide()

header = st.container()
data_and_selection = st.container()
graphs = st.container()

@st.cache
def get_data(filename):
    data = pd.read_csv(filename)
    return data
    
#header in Ukr.
with header: 

    st.title('How many candidates wrote applications and received propositions from recruiters in 30 days') 
    url = 'https://djinni.co/hire'
    btn = st.button('Find a job on Djinni :genie:')
    if btn:
       webbrowser.open_new_tab(url)

with data_and_selection: 
    st.subheader('Choose the category')
#loading data
    cand = get_data('candidates_with_pokes_applications.csv')
    cand = cand.dropna()
 #the dropdown. value = '' (defealt)
    options = cand['primary_keyword'].unique()
    options = np.insert(options,0,'')
    options = np.sort(options)
    keyword = st.selectbox('Empty choice shows all the categories together', options = options, index =0) 

    
# the function takes data and category and returns a number of candidates who wrote aplications and were poked by experience 
    def one_list(data, keyword=''):
        a = data 
        if keyword: 
            a = data[data['primary_keyword'] == keyword]
        pivoted = a.pivot_table(values = 'count', index = 'first_message', columns = 'experience', aggfunc = 'sum')
        df= pivoted.reset_index().set_index('first_message')

        cols = ['no experience','1+ year', '2+ years', '3+ years', '5+ years', '7+years']
        df = df[cols]
            
        return df

with graphs:

    #execute the function to know the skills
    df = one_list(cand, keyword = keyword)
    
    applied = df.loc["apply"].sum()
    poked = df.loc["poke"].sum()

    #st.subheader

    #st.markdown('**{}** {} candidates sent applications and **{}** candidates received propositions from recruiter over the last 30 days.'\
    #            .format(applied, keyword, poked))
    
    # variables for tick labes  
    a = (df.max().max()+df.min().min()/2)
    b = round(a/3, -1).astype(int)
    
    # number of variable
    categories=list(df)
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    fig = plt.figure(figsize=(2, 2))
    ax = fig.add_subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, fontsize =4)
    # move only one x-tick label closer to the graph
    xticklabels = ax.get_xticklabels()
    xticklabels[3].set_va('bottom')  # set the vertical alignment of the label to 'bottom'
    xticklabels[3].set_y(0.1)  # set the y-position of the label
    xticklabels[0].set_y(0.1)
   
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([b, b*2, b*3], color="grey", size=4)
    plt.ylim(0,a)

    # ------- PART 2: Add plots
    # Plot each individual = each line of the data

    # aplications
    values=df.loc["apply"].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', color = 'orange', label="Candidates \nwith applications")
    ax.fill(angles, values, 'orange', alpha=0.1)

    # pokes
    values=df.loc["poke"].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid',color = 'green', label="Candidates \nwith propositions")
    ax.fill(angles, values, 'green', alpha=0.1)

    # Add legend
    plt.legend(loc='center left', bbox_to_anchor=(1.2, 0.5), fontsize='xx-small')
    plt.title('{} {} candidates sent applications and {} candidates received propositions from recruiter over the last 30 days.'\
                .format(applied, keyword, poked), fontsize = 5)
    st.pyplot(fig)

    st.markdown('**{}** {} кандидатів писали відгуки і **{}** кандидатів отримували пропозиції від рекрутерів за останні 30 days.'\
                .format(applied, keyword, poked))
    
