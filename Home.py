import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.subheader("🔔  Analytics Dashboard")
st.markdown("##")

theme_plotly = None  #None or streamlit


#Style

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


    #load excel file
    df=pd.read_excel('gujrat.xlsx', sheet_name='Sheet1')

    #side Bar
    st.sidebar.image("data/logo1.png",caption="")
    #st.sidebar.header("BOMBAY INTEGRATED  SECURITY (INDIA) LTD")
    st.sidebar.markdown('<h1 style="color: darkred;">BOMBAY INTEGRATED SECURITY (INDIA) LTD</h1>', unsafe_allow_html=True)

    #switcher
    st.sidebar.header("Please filter")
    region=st.sidebar.multiselect(
        "Select Branch",
        options=df["Region"].unique(),
        default=df["Region"].unique(),
    )

    location=st.sidebar.multiselect(
        "Select Year",
        options=df["Location"].unique(),
        default=df["Location"].unique(),
    )

    construction=st.sidebar.multiselect(
        "Select Month",
        options=df["Construction"].unique(),
        default=df["Construction"].unique(),
    )
    df_selection=df.query(
        "Region==@region & Location==@location & Construction==@construction"
    )
def Home():
    with st.expander("⏰ My Excel WorkBook"):
        showData=st.multiselect('Filter:', df_selection.columns,default=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating"])
        st.dataframe(df_selection[showData],use_container_width=True)

    total_investment = float(df_selection['Investment'].sum())
    investment_mode = float(df_selection['Investment'].mode())
    investment_mean = float(df_selection["Investment"].mean())
    investment_median = float(df_selection["Investment"].median())
    rating = float(df_selection['Rating'].sum())

    total1,total2,total3,total4,total5=st.columns(5,gap='large')
    with total1:
        st.info('Total Investment', icon="📌")
        st.metric(label="sum TZS",value=f"{total_investment:,.0f}")

    with total2:
        st.info('Most frequent',icon="📌")
        st.metric(label="Mode TZS", value=f"{investment_mode:,.0f}")

    with total3:
        st.info('Average',icon="📌")
        st.metric(label='average TZS',value=f"{investment_mean:,.0f}")
            
    with total4:
        st.info('Central Earnings',icon="📌")
        st.metric(label="median TZS",value=f"{investment_median:,.0f}")

    with total5:
        st.info('Ratings',icon="📌")
        st.metric(label="Rating",value=numerize(rating),help=f""" Total Rating: {rating} """)

    st.markdown("""---""")

    #graphs

def graphs():

    #total_investment=int(df_selection["Investment"]).sum()
    #averageRating=int(round(df_selection["Rating"]).mean(),2)
    
    #simple bar graph
    investment_by_business_type=(
        df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
    )
    fig_investment=px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b> Investment by Business Type </b>",
        color_discrete_sequence=["#0083B8"]*len(investment_by_business_type),
        template="plotly_white",
    )

    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

        #simple line graph
    investment_state=df_selection.groupby(by=["State"]).count()[["Investment"]]
    fig_state=px.line(
       investment_state,
       x=investment_state.index,
       y="Investment",
       orientation="v",
       title="<b> Investment by State </b>",
       color_discrete_sequence=["#0083b8"]*len(investment_state),
       template="plotly_white",
    )
    fig_state.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
     )

    left,right,center=st.columns(3)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
    
    with center:
      #pie chart
      fig = px.pie(df_selection, values='Rating', names='State', title='Regions by Ratings')
      fig.update_layout(legend_title="Regions", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
     
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=3000000000
    current=df_selection["Investment"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader("Target done !")
    else:
     st.write("you have ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
     for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1,text=" Target Percentage")


def sideBar():

 with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    Home()
    graphs()
 if selected=="Progress":
    #st.subheader(f"Page: {selected}")
    Progressbar()
    graphs()

sideBar()
st.balloons()



#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

#import toml

# Load the configuration from config.toml
#config = toml.load("config.toml")

# Access theme settings

#primaryColor="#F63366"
#backgroundColor="#3d3737"
#secondaryBackgroundColor="#080707"
#textColor="#262730"
#font="sans serif"
#theme = config.get("theme", {})
#background_color = theme.get("background_color", "#3d3737")
#text_color = theme.get("text_color", "#000000")
#font_size = theme.get("font_size", 14)

# Use the theme settings in your project
#print(f"Background Color: {background_color}")
#print(f"secondary Background Color: {secondaryBackgroundColor}")
#print(f"Font Size: {font}")
