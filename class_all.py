######
import pandas as pd
from data_processing import BG_W3, W3, BG_VOICE22, VOICE22, BG_GnA, GENERAL, VOICE_NA, VOICE21, BUDGET
from st_aggrid import JsCode
from data_processing import Actual, period, sum_budget, plot_line, period_actual, format_num
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime
######

# Plans
budget = BUDGET

# budget_planned = sum_budget(budget)

# Import Class Revenue and Expenses 
w3 = W3.sort_values(by="Date")
w3['Date'] = pd.to_datetime(w3['Date'])
w3['Amount'] = w3['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))

w3_COGS = w3.loc[lambda df: df['Type']=="Expense"] 
w3_REV = w3.loc[lambda df: df['Type']=="Revenue"]


v22 = VOICE22.sort_values(by="Date")
v22['Date'] = pd.to_datetime(v22['Date'])
v22['Amount'] = v22['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))

v22_COGS = v22.loc[lambda df: df['Type']=="Expense"] 
v22_REV = v22.loc[lambda df: df['Type']=="Revenue"]


GnA = GENERAL.sort_values(by="Date")
GnA['Date'] = pd.to_datetime(GnA['Date'])
GnA['Amount'] = GnA['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))

GnA_COGS = GnA.loc[lambda df: df['Type']=="Expense"] 



v_NA = VOICE_NA.sort_values(by="Date")
v_NA['Date'] = pd.to_datetime(v_NA['Date'])
v_NA['Amount'] = v_NA['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))


v21 = VOICE21.sort_values(by="Date")
v21['Date'] = pd.to_datetime(v21['Date'])
v21['Amount'] = v21['Amount'].map(lambda Amount: float((str(Amount)).replace(",", "")))


COGS = pd.concat([w3_COGS, v22_COGS])
REV = pd.concat([w3_REV, v22_REV])
MARKET = GnA_COGS.loc[lambda df: df['Account']=="Marketing"]
LABOR = GnA_COGS.loc[lambda df: df['Account']=="Labor"] 
ADMIN =pd.concat([ GnA_COGS.loc[lambda df: df['Account']!="Labor"] , v_NA, v21])




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
exp  = budget_All[budget_All['CATEGORY']!= 'REVENUE']
exp['Q1 TOTAL'] = exp['Q1 TOTAL'].map(lambda Amount: format_num("num", Amount))
exp['Q2 TOTAL'] = exp['Q2 TOTAL'].map(lambda Amount: format_num("num", Amount))
exp['Q3 TOTAL'] = exp['Q3 TOTAL'].map(lambda Amount: format_num("num", Amount))
exp['Q4 TOTAL'] = exp['Q4 TOTAL'].map(lambda Amount: format_num("num", Amount))

rev  = budget_All[budget_All['CATEGORY']== 'REVENUE']
rev['Q1 TOTAL'] = rev['Q1 TOTAL'].map(lambda Amount: format_num("num", Amount))
rev['Q2 TOTAL'] = rev['Q2 TOTAL'].map(lambda Amount: format_num("num", Amount))
rev['Q3 TOTAL'] = rev['Q3 TOTAL'].map(lambda Amount: format_num("num", Amount))
rev['Q4 TOTAL'] = rev['Q4 TOTAL'].map(lambda Amount: format_num("num", Amount))

x_exp = exp['Q1 TOTAL'].sum()
y_exp = x_exp + exp['Q2 TOTAL'].sum()
z_exp = y_exp + exp['Q3 TOTAL'].sum()
w_exp = z_exp + exp['Q4 TOTAL'].sum()
budgeted_exp = [0, x_exp, y_exp, z_exp, w_exp]

x_rev = rev['Q1 TOTAL'].sum()
y_rev = x_rev + rev['Q2 TOTAL'].sum()
z_rev = y_rev + rev['Q3 TOTAL'].sum()
w_rev = z_rev + rev['Q4 TOTAL'].sum()
budgeted_rev = [0, x_rev, y_rev, z_rev, w_rev]

ALL_COST =pd.concat([GnA_COGS , v22_COGS, w3_COGS]).sort_values(by="Date")
REV['Date'] = pd.to_datetime(REV['Date'])
REV = REV.sort_values(by="Date")

jan_1 = datetime.datetime(2022, 1, 1, 0 ,0)
exp_p = [(_ - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's') for _ in ALL_COST['Date']]  
exp_period = [datetime.datetime.utcfromtimestamp(_) for _ in exp_p]
exp_period.insert(0, jan_1)  

exp_Amount = [_ for _ in ALL_COST['Amount']]
rev_Amount = [float(_) for _ in REV['Amount']]

rev_p = [(_ - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's') for _ in REV['Date']]
 
rev_period = [datetime.datetime.utcfromtimestamp(_) for _ in rev_p]
rev_period.insert(0, jan_1)    
amount = [0]
for i in range(len(exp_Amount)):
        amt_sum = amount[i] + exp_Amount[i]
        amount.append(amt_sum) 

rev_in = [0]
for i in range(len(rev_Amount)):
        rev_sum = rev_in[i] + rev_Amount[i]
        rev_in.append(rev_sum) 

print(rev_in)


ALL_FIG = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
ALL_FIG.add_trace(go.Scatter(x=period, y=budgeted_rev, name="Revenue Planned"),secondary_y=False,)
ALL_FIG.add_trace(go.Scatter(x=period, y=budgeted_exp, name="COGS Planned"),secondary_y=False,)
ALL_FIG.add_trace(go.Scatter(x=rev_period, y=rev_in, name="Revenue Actual"),secondary_y=False,)
ALL_FIG.add_trace(go.Scatter(x=exp_period, y=amount, name="COGS Actual"),secondary_y=False,)


# fig.add_trace(go.Scatter(x=rev[1], y=rev[0], name="Revenue Actual"),secondary_y=False,)


# fig.add_trace(go.Scatter(x=cogs[1], y=cogs[0], name="COGS Actual"),secondary_y=False,)

# Add figure title
ALL_FIG.update_layout(title_text=f"<b>All Projects</b>")

# Set x-axis title
ALL_FIG.update_xaxes(title_text="<b>Period</b> ")
# Set y-axes titles
ALL_FIG.update_yaxes(title_text="<b>Amount</b> ", secondary_y=False)


budget_All['Q1 TOTAL'] = budget_All['Q1 TOTAL'].map(lambda Amount: format_num("str", Amount))
budget_All['Q1 Actual'] = budget_All['Q1 Actual'].map(lambda Amount: format_num("str",Amount))
budget_All['Q2 TOTAL'] = budget_All['Q2 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_All['Q2 Actual'] = budget_All['Q2 Actual'].map(lambda Amount: format_num("str",Amount))
budget_All['Q3 TOTAL'] = budget_All['Q3 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_All['Q4 TOTAL'] = budget_All['Q4 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_All['Yearly'] = budget_All['Yearly'].map(lambda Amount: format_num("str",Amount))
budget_All['YTD Actual'] = budget_All['YTD Actual'].map(lambda Amount: format_num("str",Amount))