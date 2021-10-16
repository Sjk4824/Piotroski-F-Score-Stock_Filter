#!/usr/bin/env python
# coding: utf-8

# # Piotroksi F Score Code Documentation
# 
# 

# ## Importing files required for the code 
# 1. We will be using yahoo_fin [http://theautomatic.net/yahoo_fin-documentation/] library for obtaining data from Yahoo Finance. 
# 2. For data frame we will use **Pandas**. 
# 3. Additionally we will also import **math** as well as **datetime** for accesing years and correcting years. 

# In[18]:


#importing the files required for the code 
import yahoo_fin.stock_info as yf
import pandas as pd
import math
from datetime import datetime


# ## Declaring variables globally
# 1. All the data for the piotroski F score is obtained from the balance sheet, income statement and cash flow statement. 
# 2. We are delcaring these varibales globally so that it can be used in all the functions.
# 3. The data for the tickers can be imported from your local computer. *(Ensure all stocks in NSE has '.NS' as suffix and all stocks in BSE has '.BO'  as suffix.* 

# In[19]:


balance_sheet=[]
income_statement=[]
cash_flow_statement=[]
years=[]
profitability_score=0
leverage_score=0
operating_eff_score=0

#input the local file location
BSE_data= pd.read_csv('/Users/sadhanajayakumar/Desktop/Files/Webd/Piotroski_F_Score/BSE input')
tickers=BSE_data['SYMBOL WITH NS'].tolist()


final= pd.DataFrame(columns=['Ticker','Net Income','Total Assets','ROA','FROA','Operating Cash Flow','F_OP','ROA previous','F delta ROA','Accurals','F_Accurals','Profitability Score','Long term Debt','Average Assets','Leverage','Long term Debt Previous','Average Assets Previous','Leverage Previous','F Leverage','Current Ratio','Current Ratio Previous','F_Current Ratio','Leverage Score','Stock Issued Last Year','F_Stock Issuance','Total Revenue','Total Revenue Previous Year','Net Sales','Net Sales Previous Year','Margin','Margin Previous Year','F_Gross Margin','Asset Turnover Ratio','Asset Turnover Ratio Previous Year','F_Asset Turnover Ratio','Operating Efficiency Score','Piotroski Score'])


# ## Function to get data 
# With the help of the yahoo finance library, obtain all the data of balance sheet, cash flow statement, icome statement and store in their repective variables for ease in accesing the data.  

# In[20]:


#get data for above variables 
def get_data(ticker):
    global balance_sheet
    global income_statement
    global cash_flow_statement
    global  years
    balance_sheet=yf.get_balance_sheet(ticker)
    income_statement=yf.get_income_statement(ticker)
    cash_flow_statement=yf.get_cash_flow(ticker)
    years=balance_sheet.columns 


# ## Function to calculate the Profitability Score 
# 
# 1. It is important to correct the data for year. We cannot compare data for different years. In this we are going to be considering data from 2020. So check if the first year in the years[] is 2021. If it is we perform a shift and set i to 1. 
# 2. The profitiability score has 4 parameters: 
#   1. ROA Score 
#   2. Operating Cash Flow Score 
#   3. Change in ROA Score 
#   4. Accural Score
# 
# #### ROA Score 
# 1. The ROA takes 2 parameters - Net Income, Total Assets. 
# 2. If ROA>0 a score of 1 is given otherwise it is 0. 
# 
# #### Operating Cash Flow 
# 1. The operating cash flow score takes only 1 parameter that is total cash from operating activities
# 2. If the value is greater than 0 a score of 1 is given otherwise it is 0. 
# 
# #### Change in ROA 
# 1. Calculate ROA of this year which is already available, then simply calculate the ROA of the last year by changing the years[0+i] to years[1+i]. 
# 2. If the ROA of this year> ROA of last year a score of 1 is given else it is 0.
# 
# #### Accurals 
# 1. To calculate the accurals it requires 2 parameters: operating cash flow and total assets. Both the parameters are already available in the function from step 1 and 2. 
# 2. If accural> ROA a score of 1 is given, else it is given a score of 0. 
# 
# This completes all the values that are required in the profitability score. We add all the  parameters and is store it in profitability_score and return to the main call. 
# 

# In[21]:


def profitability():
    global profitability_score
    
    if(years[0].year==2021):
        i=1
    else:
        i=0
        
    global net_income
    global total_assets
    global ROA
    global F_ROA
    
    
    net_income= income_statement[years[0+i]]['netIncome']
    total_assets=balance_sheet[years[0+i]]['totalAssets']
    ROA=  net_income/total_assets
    if(ROA>0):
        F_ROA=1;
    else:
        F_ROA=0;
    
    #Operating Cash Flow
    global operatingCashFlow
    global F_CFO
    
    operatingCashFlow= cash_flow_statement[years[0+i]]['totalCashFromOperatingActivities']
    if(operatingCashFlow>0):
        F_CFO=1
    else:
        F_CFO=0
        
    #change in ROA
    global ROA_py
    global F_delta_ROA
    
    net_income_py= income_statement[years[i+1]]['netIncome']
    total_assets_py=balance_sheet[years[i+1]]['totalAssets']
    ROA_py = net_income_py/total_assets_py
    if(ROA>ROA_py):
        F_delta_ROA=1
    else:
        F_delta_ROA=0
        
    #accurals
    global accural
    global F_Accural
    
    accural= operatingCashFlow/total_assets
    if(accural> ROA):
        F_Accural=1
    else:
        F_Accural=0
    
    profitability_score= F_ROA+ F_CFO+ F_delta_ROA+ F_Accural
    return profitability_score
    #print(profitability_score)
    
    


# ## Function to calculate the Leverage Score
# 
# 1. It is important to correct the data for year. We cannot compare data for different years. In this we are going to be considering data from 2020. So check if the first year in the years[] is 2021. If it is we perform a shift and set i to 1.
# 2. The leverage score has 3 parameters. 
#     1. Change in Leverage 
#     2. Change in Current Ratio 
#     3. Change in Number of Shares
# 
# #### Change in leverage 
# 1. To calculate the change in leverage we need long term debt of this year and last year, total assets of this year and last year. 
# 2. If the leverage of this year is greater than last year we assign a score of 0 else we give a score of 1
# 
# #### Change in current ratio
# 1. To calculate the current ratio it needs only 2 parameters: total assets and total liabilities. Calculate for this year and last year and find the difference. 
# 2. If current ratio of this year is greater than that of last year we give a score of 1 else it is 0. 
# 
# #### Change in the number of shares 
# 1. We need to find the number of stocks that were issued last year and last last year and find their difference. If the difference is less than or equal to 0, it means that the company didnt issue any new shares and give a score of 1 else it is given a score of 0. 
# 
# This completes all the values that are required in the leverage score. We add all the parameters and is store it in leverage_score and return to the main call.

# In[22]:


def leverage():
    global leverage_score
    
    if(years[0].year==2021):
        i=1
    else:
        i=0
    
    #change in leverage
    global long_term_debt
    global average_assets
    global lev
    global long_term_debt_py
    global average_assets_py
    global lev_py
    global F_Leverage
    
    long_term_debt= balance_sheet[years[0+i]]['totalLiab']- balance_sheet[years[0+i]]['totalCurrentLiabilities']
    average_assets=(balance_sheet[years[0+i]]['totalAssets']+balance_sheet[years[1+i]]['totalAssets'])/2
    lev= long_term_debt/average_assets
    long_term_debt_py=  balance_sheet[years[1+i]]['totalLiab']- balance_sheet[years[1+i]]['totalCurrentLiabilities']
    average_assets_py=(balance_sheet[years[1+i]]['totalAssets']+ balance_sheet[years[2+i]]['totalAssets'])/2
    lev_py= long_term_debt_py/average_assets_py
    if(lev<lev_py):
        F_Leverage=1
    else:
        F_Leverage=0
        
    #Change in current ratio
    global current_ratio
    global current_ratio_py
    global F_Current_Ratio
    
    current_ratio= balance_sheet[years[0+i]]['totalCurrentAssets']/ balance_sheet[years[0+i]]['totalCurrentLiabilities']
    current_ratio_py= balance_sheet[years[1+i]]['totalCurrentAssets']/ balance_sheet[years[1+i]]['totalCurrentLiabilities']
    if(current_ratio>current_ratio_py):
        F_Current_Ratio= 1
    else:
        F_Current_Ratio= 0
        
    #change in the number of shares
    global stock_issued
    global F_Stock_Issuance
    
    stock_issued= balance_sheet[years[1+i]]['commonStock']-balance_sheet[years[2+i]]['commonStock']
    if(stock_issued<=0):
        F_Stock_Issuance=1
    else:
        F_Stock_Issuance=0
        
    leverage_score= F_Leverage+ F_Current_Ratio+ F_Stock_Issuance
    return leverage_score
   # print(leverage_score)


# ## Function to calculate the Operating Efficiency Score 
# 
# 1. It is important to correct the data for year. We cannot compare data for different years. In this we are going to be considering data from 2020. So check if the first year in the years[] is 2021. If it is we perform a shift and set i to 1.
# 2. The operating efficiency score has 2 parameters:
#     1. Change in Gross Margin 
#     2. Change in asset turn over ratio
# 
# #### Change in gross margin 
# 1. The gross margin requires 2 prameters for caluclating that is: total revenue and gross profit. Calculate the gross profit for this year and the previous, if it is greater for the current year compared to the previous year, we assign a score of 1, else it is given a score of 0. 
# 
# #### Change in asset turnover ratio 
# 1. To calculate the asset turnover ratio, we need 2 parameters: total revenue and average assets. 
# 2. Find the difference between the asset turn over ratio of this year and the previous year. 
# 3. If its greater for the current year a score of 1 is given else  a score of 0 is given. 
# 
# This completes all the values that are required in the operating efficiency score, we add all the parameters and store it in operating_eff_score and return to the main call.

# In[23]:


def operating_eff():
    global operating_eff_score
    
    if(years[0].year==2021):
        i=1
    else:
        i=0
    
    #change in gross margin 
    global total_revenue
    global total_revenue_py
    global sales
    global sales_py
    global margin
    global margin_py
    global F_Gross_Margin 
    
    total_revenue= income_statement[years[0+i]]['totalRevenue']
    total_revenue_py= income_statement[years[1+i]]['totalRevenue']
    sales= income_statement[years[0+i]]['grossProfit']
    sales_py= income_statement[years[1+i]]['grossProfit']
    margin= (total_revenue- sales)/total_revenue
    margin_py= (total_revenue_py- sales_py)/total_revenue_py
    if(margin> margin_py):
        F_Gross_Margin=1
    else:
        F_Gross_Margin=0
        
    #Change in asset turnover ratio
    global asset_turn_over
    global asset_turn_over_py
    global F_Asset_Turnover
    
    average_assets=(balance_sheet[years[0+i]]['totalAssets']+balance_sheet[years[1+i]]['totalAssets'])/2
    average_assets_py=(balance_sheet[years[1+i]]['totalAssets']+ balance_sheet[years[2+i]]['totalAssets'])/2
    asset_turn_over= total_revenue/average_assets
    asset_turn_over_py= total_revenue_py/average_assets_py
    if(asset_turn_over> asset_turn_over_py):
        F_Asset_Turnover=1
    else:
        F_Asset_Turnover=0
        
    operating_eff_score= F_Gross_Margin+ F_Asset_Turnover
    return operating_eff_score
    
    


# ## Loop to run the code for all the stocks in the imported file. 
# 
# 1. From the file we extract the data for the tickers and the company name. For simultaneously iterating over the both the lists we use the python zip function and set the ranges according to the number of stocks you want to run it for. 
# 2. If some parameter for the code is not available the control goes to the except funtion and sets all the data for the stock to NA, this is done to prevent the loop from terminating in the middle. 
# 3. All the variables are intially stored into a dictionary and appended as new rows. 
# 4. This is then converted to a Pandas Data frame.  The output is stored to a csv file and can be accessed on your local computer. 

# In[24]:


#runnning the loop for tickers
for ticker in tickers[0:3]:
    try:
        get_data(ticker)
        pro= profitability()
        leverageRatio=leverage()
        op=operating_eff()
        #print('Profitability is: ' + str(pro)
        total= pro+leverageRatio+op
        new_row= {'Ticker':ticker,
                  'Net Income':net_income,
                  'Total Assets':total_assets,
                  'ROA':ROA,
                  'FROA':F_ROA,
                  'Operating Cash Flow':operatingCashFlow,
                  'F_OP':F_CFO,
                  'ROA previous':ROA_py,
                  'F delta ROA':F_delta_ROA,
                  'Accurals':accural,
                  'F_Accurals':F_Accural,
                  'Profitability Score':pro,
                  'Long term Debt':long_term_debt ,
                  'Average Assets':average_assets ,
                  'Leverage':lev,
                  'Long term Debt Previous':long_term_debt_py,
                  'Average Assets Previous':average_assets_py,
                  'Leverage Previous':lev_py,
                  'F Leverage':F_Leverage,
                  'Current Ratio':current_ratio,
                  'Current Ratio Previous':current_ratio_py,
                  'F_Current Ratio':F_Current_Ratio, 
                  'Leverage Score':leverageRatio,
                  'Stock Issued Last Year':stock_issued,
                  'F_Stock Issuance': F_Stock_Issuance,
                  'Total Revenue':total_revenue,
                  'Total Revenue Previous Year':total_revenue_py,
                  'Net Sales':sales, 
                  'Net Sales Previous Year':sales_py, 
                  'Margin':margin, 
                  'Margin Previous Year':margin_py,
                  'F_Gross Margin':F_Gross_Margin,
                  'Asset Turnover Ratio':asset_turn_over,
                  'Asset Turnover Ratio Previous Year':asset_turn_over_py,
                  'F_Asset Turnover Ratio':F_Asset_Turnover, 
                  'Operating Efficiency Score':op,
                  'Piotroski Score':total}
        final= final.append(new_row, ignore_index=True)
        print(ticker+' Added')           
            
    except:
        new_row= {'Ticker':ticker,
                  'Net Income':'NA',
                  'Total Assets':'NA',
                  'ROA':'NA',
                  'FROA':'NA',
                  'Operating Cash Flow':'NA',
                  'F_OP':'NA',
                  'ROA previous':'NA',
                  'F delta ROA':'NA',
                  'Accurals':'NA',
                  'F_Accurals':'NA',
                  'Profitability Score':'NA',
                  'Long term Debt':'NA' ,
                  'Average Assets':'NA' ,
                  'Leverage':'NA',
                  'Long term Debt Previous':'NA',
                  'Average Assets Previous':'NA',
                  'Leverage Previous':'NA',
                  'F Leverage':'NA',
                  'Current Ratio':'NA',
                  'Current Ratio Previous':'NA',
                  'F_Current Ratio':'NA', 
                  'Leverage Score':'NA',
                  'Stock Issued Last Year':'NA',
                  'F_Stock Issuance': 'NA',
                  'Total Revenue':'NA',
                  'Total Revenue Previous Year':'NA',
                  'Net Sales':'NA', 
                  'Net Sales Previous Year':'NA', 
                  'Margin':'NA', 
                  'Margin Previous Year':'NA',
                  'F_Gross Margin':'NA',
                  'Asset Turnover Ratio':'NA',
                  'Asset Turnover Ratio Previous Year':'NA',
                  'F_Asset Turnover Ratio':'NA', 
                  'Operating Efficiency Score':'NA',
                  'Piotroski Score':'NA'}
        final= final.append(new_row, ignore_index=True)
        print(ticker+' Added')
        


# #### To view the data you have obtained so far run the below code to display the data frame.
# 
# An example of the how the data frmae looks is given below 

# In[25]:


final


# #### To save the dataframe data as a '.csv' file in your computer use the below command and specify the location where you want to store it. 

# In[9]:


final.to_csv('/Users/sadhanajayakumar/Desktop/piotroski/asasas.csv',index=False)

