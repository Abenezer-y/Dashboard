######
from lib2to3.pgen2.token import GREATER
import streamlit as st
import pandas as pd 
import datetime
import requests
import json
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
import plotly.graph_objects as go
import time
import plotly.express as px
from class_voice22 import v22_fig, budget_v22, v22_REV, v22_COGS 
from class_w3 import  w3_fig, budget_w3, w3_REV, w3_COGS 
from class_all import  budget_All, COGS, REV , All_jscode

from class_general import  gna_fig, budget_gna, gna_REV, gna_COGS, bdg_GnA, df_gen, Q2_DF,  Q1_DF
from data_processing import Account_Balance, format, week_range, convert_to_df, Grid, get_data, date_formatter, budget_GnA
from data_processing import cashflow, get_upWork, get_credit, get_bank, get_data, get_sales, get_budget, get_accounts, get_loan, get_receivables, get_payables, get_sponsorship, get_payroll, get_general, get_voice21, get_voice22, get_voiceNA, get_w3
######

# st.set_page_config(layout="wide")
#####################################
######## Utility Constants ##########
headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}
jan_1 = datetime.datetime(2022, 1, 1, 0, 0, 0)
today = datetime.datetime.today()
reports = ["Cash Flow", "Budget Reconciliation",]
periods = ["Current Week", "Previous Week", "Year to Date"]
projects = ["All", "Voice Summit 2022", "W3", "G&A"]
indices = [1, 2, 3, 4, 5]
income = {}
receivable = {}
#####################################
#####################################

###########################################################################
################################### UI ####################################

#####################################
############## SIDEBAR ##############
sideBar = st.sidebar
sideBar.title("Control Panel")
report = sideBar.selectbox('Reports', options=reports)

sideBar.header("Filters")
if report == "Cash Flow":
    project = sideBar.selectbox('Classes', options=projects)
    period = sideBar.selectbox('Period', options=periods)
elif report == "Budget Reconciliation":
    project = sideBar.selectbox('Classes', options=projects)
#####################################
#####################################
CONTAINER = st.container()

#####################################
############# CASHFLOW ##############
if report == 'Cash Flow':
    CONTAINER.title("MODEV Cash Flow Report")

    if period == 'Current Week':
        CONTAINER.header('Cash Flow Summary - Current Week')
        days = week_range(1)
        cash = cashflow(days[0], days[1])
        Cash = Grid(cash.iloc[indices], key='key_872w1', h=400)

    elif period == 'Previous Week':
        CONTAINER.header('Cash Flow Summary - Previous Week')
        days = week_range(2)
        cash = cashflow(days[0], days[1])
        Cash = Grid(cash.iloc[indices], key='key_87991',  h=400)

    elif period == 'Year to Date':
        CONTAINER.header('Cash Flow Summary - Year to Date')
        cash = cashflow(jan_1, today)
        Cash = Grid(cash, key='key_87dd991',  h=550)
#####################################
#####################################

#####################################
######## Budget Utilization #########
elif report == 'Budget Reconciliation':
    if project == 'All':
        CONTAINER.title("MODEV Planned Budget vs Actual - All Classes")
        CONTAINER.plotly_chart(v22_fig, use_container_width=True)
        
        bg_all = Grid(budget_All, key='All', h=400, p=False)
    elif project == 'G&A':
        CONTAINER.title("MODEV Planned Budget vs Actual - General and Admin")
        CONTAINER.plotly_chart(gna_fig, use_container_width=True)
        
        bg_gna = Grid(bdg_GnA, key='G&A',  p=False, h=330)
        st.info('Total Budget for Non Project Costs:  {:,.2f}'.format(bg_gna['data']['Yearly'].sum()))
        # Q2_DF,  Q1_DF
        with st.expander("General and Admin Costs Detail"):
            accs = budget_GnA['Account'].unique()
            c5, c6, c7, c8, c9 = st.columns(5)
            cols = ["Detail", "Yearly"]
            budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float(str(Amount).replace(",", ""))))
            with c5:
                c5.write(accs[0])
                Exp_0 = Grid(budget_GnA[budget_GnA['Account']==accs[0]][cols], key=accs[0], h=400,  p=False)
                st.info('Total Balance:  {:,.2f}'.format((Exp_0['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum()))
            with c6:
                c6.write(accs[1])
                budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float((str(Amount)).replace(",", ""))))
                Exp_1 = Grid(budget_GnA[budget_GnA['Account']==accs[1]][cols], key=accs[1], h=400,  p=False)
                st.info('Total Balance:  {:,.2f}'.format((Exp_1['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum()))
            with c7:
                c7.write(accs[2])
                budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float((str(Amount)).replace(",", ""))))
                Exp_2 = Grid(budget_GnA[budget_GnA['Account']==accs[2]][cols], key=accs[2], h=400,  p=False)
                st.info('Total Balance:  {:,.2f}'.format((Exp_2['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum()))
            with c8:
                c8.write(accs[3])
                budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float((str(Amount)).replace(",", ""))))
                Exp_3 = Grid(budget_GnA[budget_GnA['Account']==accs[3]][cols], key=accs[3], h=400,  p=False)
                st.info('Total Balance:  {:,.2f}'.format((Exp_3['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum()))
            with c9:
                c9.write(accs[4])
                budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float((str(Amount)).replace(",", ""))))
                Exp_4 = Grid(budget_GnA[budget_GnA['Account']==accs[4]][cols], key=accs[4],  h=400,  p=False)
                st.info('Total Balance:  {:,.2f}'.format((Exp_4['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum()))


# budget_GnA
    elif project == 'Voice Summit 2022':

        CONTAINER.title("MODEV Planned Budget vs Actual - Voice Summit 2022")
        CONTAINER.plotly_chart(v22_fig, use_container_width=True)

        bg_v22 = Grid(budget_v22, key='Voice22',  h=200, p=False)
        c1, c2 = st.columns(2)
        with c1:
            c1.header("COGS")
            v22_COGS_df = Account_Balance(v22_COGS)
            v22_COGS_df['Balance'] = v22_COGS_df['Balance'].map(lambda Amount: "{:,.2f}".format(Amount))
            V22_Exp = Grid(v22_COGS_df, key='V22_Exp', h=400, p=False)
            st.info('Total Balance:  {:,.2f}'.format((V22_Exp['data']['Balance'].map(lambda Amount: float(Amount.replace(",","")))).sum()))
        with c2:
            c2.header("Revenue")
            v22_REV['Amount'] = v22_REV['Amount'].map(lambda Amount: "{:,.2f}".format(float(Amount.replace(",",""))))
            V22_SP = Grid(v22_REV[["Vendor", "Account", "Amount"]], key='V22_SP', h=400, p=False)
            st.info('Total Balance:  {:,.2f}'.format((V22_SP['data']['Amount'].map(lambda Amount: float(Amount.replace(",","")))).sum()))
            # st.info('Total Balance:  {:,.2f}'.format(V22_SP['data']['Amount'].sum()))
    ########
    elif project == 'W3':

        CONTAINER.title("MODEV Planned Budget vs Actual - W3")
        CONTAINER.plotly_chart(w3_fig, use_container_width=True)

        bg_w3 = Grid(budget_w3, key='W3',  h=200, p=False)
        c3, c4 = st.columns(2)

        with c3:
            c3.header("COGS")
            W3_Exp = Grid(Account_Balance(w3_COGS), key='W3_Exp', h=400, p=False)
            st.info('Total Balance:  {:,.2f}'.format(W3_Exp['data']['Balance'].sum()))
        with c4:
            st.header("Revenue")
            W3_SP = Grid(w3_REV[["Vendor", "Account", "Amount"]], key='W3_SP', h=400, p=False)
            st.info('Total Balance:  {:,.2f}'.format(W3_SP['data']['Amount'].sum()))
#####################################
#####################################