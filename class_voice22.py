######
from data_processing import BG_VOICE22, VOICE22
from data_processing import Actual, period, sum_budget, plot_line, period_actual
######

# Plans
budget_v22 = BG_VOICE22
v22_planned = sum_budget(budget_v22)

# Import Class Revenue and Expenses 
v22 = VOICE22
v22_COGS = v22[v22['Type']=="Expense"]
v22_REV = v22[v22['Type']=="Revenue"]

# Actual COGS and Revenue
v22_cogs = Actual(v22_COGS)
v22_rev = Actual(v22_REV)

# Draw Plot and Update Budget
v22_fig = plot_line(period, planned=v22_planned, rev=v22_rev, cogs=v22_cogs, title="Financial Performace for Voice 2022")


budget_v22 = period_actual(budget_v22, v22_REV, v22_COGS, period)