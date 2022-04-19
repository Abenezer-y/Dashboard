######
import pandas as pd
from data_processing import BG_W3, W3, BG_VOICE22, VOICE22, BG_GnA, GENERAL, VOICE_NA, VOICE21, BUDGET
from st_aggrid import JsCode
from data_processing import Actual, period, sum_budget, plot_line, period_actual
######

# Plans
budget = BUDGET

# budget_planned = sum_budget(budget)

# Import Class Revenue and Expenses 
w3 = W3
w3['Date'] = pd.to_datetime(w3['Date'])
w3_COGS = w3[w3['Type']=="Expense"]
w3_REV = w3[w3['Type']=="Revenue"]
w3_REV['Amount'] = w3_REV['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))
w3_COGS['Amount'] = w3_COGS['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))

v22 = VOICE22
v22['Date'] = pd.to_datetime(v22['Date'])
v22_COGS = v22[v22['Type']=="Expense"]
v22_COGS['Amount'] = v22_COGS['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))
v22_REV = v22[v22['Type']=="Revenue"]
v22_REV['Amount'] = v22_REV['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))

GnA = GENERAL
GnA['Date'] = pd.to_datetime(GnA['Date'])
GnA_COGS = GnA[GnA['Type']=="Expense"]
GnA_COGS['Amount'] = GnA_COGS['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))


v_NA = VOICE_NA
v_NA['Date'] = pd.to_datetime(v_NA['Date'])
v_NA_COGS = v_NA[v_NA['Type']=="Expense"]
v_NA_COGS['Amount'] = v_NA_COGS['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))


v21 = VOICE21
v21['Date'] = pd.to_datetime(v21['Date'])
v21_COGS = v21[v21['Type']=="Expense"]
v21_COGS['Amount'] = v21_COGS['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))


COGS = pd.concat([w3_COGS, v22_COGS])
REV = pd.concat([w3_REV, v22_REV])
MARKET = GnA_COGS[GnA_COGS["Account"]=="Marketing"]
LABOR = GnA_COGS[GnA_COGS["Account"]=="Labor"]
ADMIN =pd.concat([ GnA_COGS[GnA_COGS["Account"]!="Labor"], v_NA_COGS, v21_COGS])

# df['Date'] = pd.to_datetime(df['Date'])
COGS = COGS.sort_values(by="Date")
REV = REV.sort_values(by="Date")
MARKET = MARKET.sort_values(by="Date")
LABOR = LABOR.sort_values(by="Date")
ADMIN = ADMIN.sort_values(by="Date")


COGS_All = Actual(COGS)
REV_All = Actual(REV)
MARKET_All = Actual(MARKET)
LABOR_All = Actual(LABOR)
ADMIN_All = Actual(ADMIN)

w3_cogs = Actual(w3_COGS)
budget["Q1 Actual"] = [REV[REV['Date']<=period[1]]['Amount'].sum(), COGS[COGS['Date']<=period[1]]['Amount'].sum(), MARKET[MARKET['Date']<=period[1]]['Amount'].sum(), LABOR[LABOR['Date']<=period[1]]['Amount'].sum(), ADMIN[ADMIN['Date']<=period[1]]['Amount'].sum()]

budget["Q2 Actual"] = [REV[(REV['Date']>period[1])&(REV['Date']<=period[2])]['Amount'].sum(), COGS[(COGS['Date']>period[1])&(COGS['Date']<=period[2])]['Amount'].sum(), MARKET[(MARKET['Date']>period[1])&(MARKET['Date']<=period[2])]['Amount'].sum(), 
                       LABOR[(LABOR['Date']>period[1])&(LABOR['Date']<=period[2])]['Amount'].sum(), ADMIN[(ADMIN['Date']>period[1])&(ADMIN['Date']<=period[2])]['Amount'].sum()]

budget["YTD Actual"] = [REV['Amount'].sum(), COGS['Amount'].sum(), MARKET['Amount'].sum(), LABOR['Amount'].sum(), ADMIN['Amount'].sum()]
bgt_cols = ["CATEGORY", "Q1 TOTAL", "Q1 Actual", "Q2 TOTAL", "Q2 Actual", "Q3 TOTAL", "Q4 TOTAL", "Yearly", "YTD Actual"]
for col in ['Q1 Actual', "Q2 Actual", "YTD Actual",]:
    budget[col] = budget[col].map(lambda Amount: "{:,.2f}".format(Amount))
budget_All = budget[bgt_cols]
# Draw Plot and Update Budget
# all_fig = plot_line(period, planned=budget_planned, title="Financial Performace for W3", rev=None, cogs=w3_cogs)
# budget_all = period_actual(budget, w3_REV, w3_COGS, period)
All_jscode = JsCode("""
        function(params){

                return {
                    'color': 'black',
                    'backgroundColor' : 'orange'

            }
            
       
    };
    """)