import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("NFL Football Stats (Rushing) Explorer")

st.markdown("""
Esta aplicacion desarrolla  webscraping  de NFL Football Player  stats data(focusing on Rushing)!
* **Librerias Python:** base64, pandas, streamlit
* **Data source:** [pro-football-reference](https://www.pro-football-reference.com/years/2022/rushing.htm)

""")

# st.title
# st.markdown
# st.header
# st.write
# st.dataframe
# Download
# st.markdown
#sidebar
# st.sidebar.header **********
# st.sidebar.selectbox ***********
# st.sidebar.multiselect ***********
# st.sidebar.multiselect ***********
# heatmap
# st.button
# st.header
# st.pyplot
st.sidebar.header("User Input Features")

selected_year = st.sidebar.selectbox('Year',list(reversed(range(1990,2021))))

# Web Scraping NFL player stats
# https://pro-football-reference.com/years/2021/rushing.htm
@st.cache_data
def load_data(year):
    url  = "https://www.pro-football-reference.com/years/"+str(year)+"/rushing.htm"
    html = pd.read_html(url,header=1)
    df   = html[0]
    raw  = df.drop(df[df.Age=='Age'].index) # Deletes repeating headers in content
    raw  = raw.fillna(0)
    playerstats  = raw.drop(['Rk'],axis=1)
    return playerstats


playerstats  = load_data(selected_year)

# Sidebar- Team Selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team      = st.sidebar.multiselect('Team',sorted_unique_team,sorted_unique_team)

# Sidebar - Position Selection
unique_pos         = ['RB','QB','WB','FB','TE']
selected_pos       = st.sidebar.multiselect('Position',unique_pos,unique_pos)

# FILTERING DATA
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team))&(playerstats.Pos.isin(selected_pos))]

st.header('Display Plater Stats of Selected Team(s)')
st.write('Data Dimension: '+ str(df_selected_team.shape[0])+' rows and '+str(df_selected_team.shape[1])+' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlite.io/t/how-to-download-file-in-streanlit/1806
def filedownload(df):
    csv  = df.to_csv(index = False)
    b64  = base64.b64encode(csv.encode()).decode() # strings <-> bytes conversion
    href = f'<a href="data:file/csv;base64,{b64}" download = "playerstats.csv">Download CSV File </a>'
    return href

st.markdown(filedownload(df_selected_team),unsafe_allow_html=True)

# heatmap
if st.button('Intercorrelation Heatmap'):
   st.header('Intercorrelation Matrix Heatmap')
   df_selected_team.to_csv('output.csv',index= False)
   df = pd.read_csv('output.csv')
   df = df.select_dtypes(include=[float,int])
   corr = df.corr()
   mask = np.zeros_like(corr)
   mask[np.triu_indices_from(mask)] = True
   with sns.axes_style("white"):
        f,ax = plt.subplots(figsize=(7,5))
        ax   = sns.heatmap(corr,mask=mask,vmax=1,square=True)
   st.pyplot(f)
