######
from data_processing import BG_VOICE22, VOICE22
from data_processing import Actual, period, sum_budget, plot_line, period_actual, format_num
######

# Plans
budget_v22 = BG_VOICE22
v22_planned = sum_budget(budget_v22)

# Import Class Revenue and Expenses 
# v22 = VOICE22
v22_COGS = VOICE22.loc[lambda df: df['Type']=="Expense"]
v22_REV = VOICE22.loc[lambda df: df['Type']=="Revenue"]

# Actual COGS and Revenue
v22_cogs = Actual(v22_COGS)
v22_rev = Actual(v22_REV)

# Draw Plot and Update Budget
v22_fig = plot_line(period, planned=v22_planned, rev=v22_rev, cogs=v22_cogs, title="Financial Performace for Voice 2022")


budget_v22 = period_actual(budget_v22, v22_REV, v22_COGS, period)
budget_v22['Q1 TOTAL'] = budget_v22['Q1 TOTAL'].map(lambda Amount: format_num("str", Amount))
budget_v22['Q1 Actual'] = budget_v22['Q1 Actual'].map(lambda Amount: format_num("str",Amount))
budget_v22['Q2 TOTAL'] = budget_v22['Q2 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_v22['Q2 Actual'] = budget_v22['Q2 Actual'].map(lambda Amount: format_num("str",Amount))
budget_v22['Q3 TOTAL'] = budget_v22['Q3 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_v22['Q4 TOTAL'] = budget_v22['Q4 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_v22['Yearly'] = budget_v22['Yearly'].map(lambda Amount: format_num("str",Amount))
budget_v22['YTD Actual'] = budget_v22['YTD Actual'].map(lambda Amount: format_num("str",Amount))