import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from datetime import datetime
import calendar



st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.subheader("🔔  Performance Metrics for Gujrat CAD")
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
    st.sidebar.markdown('<h1 style="color: white;">BOMBAY INTEGRATED SECURITY (INDIA) LTD</h1>', unsafe_allow_html=True)

    #Report Type
    options = ['Monthly', 'Yearly']
    report_type=st.sidebar.radio("Select Report Type",options)

    #switcher
    st.sidebar.header("Please filter")
    brLocName=st.sidebar.multiselect(
        "Select Branch",
        options=df["BrLocName"].unique(),
        default=df["BrLocName"].unique(),
    )

    invoiceYear=st.sidebar.multiselect(
        "Select Year",
        options=df["InvoiceYear"].unique(),
        default=df["InvoiceYear"].unique(),
    )
    if report_type == 'Yearly':
        invoiceMonth=st.sidebar.multiselect(
            "Select Month",
            options=df["InvoiceMonth"].unique(),
            default=df["InvoiceMonth"].unique(),
        )
    else:
   
        invoiceMonth=st.sidebar.selectbox(
            "Select Month",
            options=df["InvoiceMonth"].unique()[::-1]
            #default=df["InvoiceMonth"].head(1).unique(),
          
        )
        if invoiceMonth == 'January':
            monthNumber=1
        elif invoiceMonth == 'February':
            monthNumber=2
        elif invoiceMonth == 'March':
            monthNumber=3
        elif invoiceMonth == 'April':
            monthNumber=4
        elif invoiceMonth == 'May':
            monthNumber=5
        elif invoiceMonth =='June':
            monthNumber=6
        elif invoiceMonth == 'July':
            monthNumber=7
        elif invoiceMonth == 'August':
            monthNumber=8
        elif invoiceMonth == 'September':
            monthNumber=9
        elif invoiceMonth == 'October':
            monthNumber=10
        elif invoiceMonth == 'November':
            monthNumber=11
        elif invoiceMonth == 'December':
            monthNumber=12

    df_selection=df.query(
        "BrLocName==@brLocName & InvoiceYear==@invoiceYear & InvoiceMonth==@invoiceMonth"
    )
def Home():
    with st.expander("⏰ My Excel WorkBook"):
        showData=st.multiselect('Filter:', df_selection.columns,default=["BrLocName","CADNAME","InvoiceYear","InvoiceMonth","InvoiceNo","InvType","CustName","InvoiceAmount","InvTotalDtlAmt","InvTotalDtlOCAmt","Invoice_Month"])
        st.dataframe(df_selection[showData],use_container_width=True)




    df_selection['InvoiceAmount'] = pd.to_numeric(df_selection['InvoiceAmount'], errors='coerce')

    # Calculate the statistics
    total_invoice_amount = df_selection['InvoiceAmount'].sum()
    

    invoice_count = df_selection['InvoiceNo'].count()
    if report_type == 'Monthly':
        count_of_invoices = len(df.loc[df["Invoice_Month"] == int(monthNumber-1)])
        diff = (invoice_count - count_of_invoices )
        previous_month_Amount= df[df["Invoice_Month"]==int(monthNumber-1)]["InvoiceAmount"].sum()
        Amount_Diff = (total_invoice_amount - previous_month_Amount)
    

    if report_type == 'Monthly':
        
        total1,total2,total3,total4=st.columns(4,gap='large')
        with total1:
            st.info('Invoice Count Summary', icon="📌")
            st.metric(label="Invoice Count Summary",value=f"🧾 {invoice_count:,.0f}")

        with total2:
            st.info('Invoice Quantity Variations',icon="📌")
            st.metric(label="Invoice Quantity Variations", value=f"🖆 {diff:,.0f}")

        with total3:
            st.info('Total Invoice Value',icon="📌")
            st.metric(label="Total Invoice Value",value=f"💰 {total_invoice_amount:,.0f}")

            
        with total4:
            st.info('Variation in Total',icon="📌")
            if Amount_Diff<0:
                st.metric(label="Variation in Total",value=f"🔴 {Amount_Diff:,.0f}")
            else:
                st.metric(label="Variation in Total",value=f"🟢 {Amount_Diff:,.0f}")


        #with total5:
            #st.info('Average',icon="📌")
            #st.metric(label='average TZS',value=f"{investment_mean:,.0f}")
    else:
        total1,total3=st.columns(2,gap='large')
        with total1:
            st.info('Invoice Count Summary', icon="📌")
            st.metric(label="Invoice Count Summary",value=f"🧾 {invoice_count:,.0f}")

        with total3:
            st.info('Total Invoice Value',icon="📌")
            st.metric(label="Total Invoice Value",value=f"💰 {total_invoice_amount:,.0f}")

        #with total4:
            #st.info('Central Earnings',icon="📌")
            #st.metric(label="median TZS",value=f"{investment_median:,.0f}")

       

    st.markdown("""---""")

    #graphs

def graphs():
    customer_total_invoices = df_selection.groupby("CustName")["InvoiceAmount"].sum()
    sorted_customers = customer_total_invoices.sort_values(ascending=False)
    top_10_customers = sorted_customers.head(10)
    top_10_customers_df = pd.DataFrame({
        "Customer Identification": top_10_customers.index,
        "Invoice Sum Summary": top_10_customers.values,
        "color":["#1E90FF","#0083B8", "#00FF00", "#FF5733", "#FFD700", "#FF1493", "#8A2BE2", "#FFA07A",  "#FF6347", "#40E0D0"] 
    })


# Create a bar chart using Plotly Express
    fig_investment = px.bar(
        top_10_customers_df,
        x="Invoice Sum Summary",
        y="Customer Identification",
        orientation="h",
        title="<b> Top 10 Invoice Clients </b>",
        #color_discrete_sequence=["#0083B8"] * len(top_10_customers_df),
        color="color",
        template="plotly_white"
    )

    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=(dict(showgrid=False))
    )
    right,center=st.columns(2)
    if report_type == 'Yearly':
        left,right,center=st.columns(3)
        #simple line graph
        
        investment_state = df.groupby(by=["InvoiceMonth"])["InvoiceAmount"].sum().reset_index()
        custom_month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Create the histogram chart
        fig_state = px.scatter(
            investment_state,
            x="InvoiceMonth",
            y="InvoiceAmount",
            title="<b>Amount Trends by Month </b>",
            size="InvoiceAmount",
            color="InvoiceAmount",
            #color_discrete_sequence=["#0083b8"] * len(investment_state),
            color_discrete_sequence=px.colors.qualitative.Set1,
            template="plotly_white",
        )

        fig_state.update_layout(
            xaxis=dict(categoryorder="array", tickmode="array", categoryarray=custom_month_order),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=False)
        )

    
        left.plotly_chart(fig_state,use_container_width=True)
    #right.plotly_chart(fig_investment,use_container_width=True)
    #right.plotly_chart(fig_investment, use_container_width=True)
    
    with right:
       st.plotly_chart(fig_investment, use_container_width=True)

    with center:
      #pie chart
      fig = px.pie(df_selection, values='InvoiceAmount', names='BrLocName', title='Branch-wise Performance')
      fig.update_layout(legend_title="Branch", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

   


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
 #if selected=="Progress":
    #st.subheader(f"Page: {selected}")
    #Progressbar()
    #graphs()

sideBar()
#st.balloons()



#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

