# %%
import pandas as pd
from datetime import datetime
# %%
# Reading the data
ae_df = pd.read_excel("AE_data_sample.xlsx", engine='openpyxl', sheet_name='Sheet1')
ae_df.to_csv('ae_df.csv')
cm_df = pd.read_excel("cm_data_sample.xlsx", engine='openpyxl', sheet_name='Sheet1')
cm_df.to_csv('cm_df.csv')
ae_headers_df = pd.read_excel("Hackathon Data Dictionary.xlsx", engine='openpyxl', sheet_name='AE Dictionary')
cm_headers_df = pd.read_excel("Hackathon Data Dictionary.xlsx", engine='openpyxl', sheet_name='CM Dictionary')
# %%

# Joining the data
required_columns = ['AETERM', 'AESTDAT', 'AESPID', 'AEENDAT', 'AETOXGR', 'AECM', 'CMTRT', 'CMSTDAT', 'CMENDAT', 'CMAENO', 'SUBJID', 'SITEID']

ae_columns = set(ae_df.columns)
ae_req_col = ae_columns.intersection(required_columns)
ae_req_df = ae_df[ae_req_col]

cm_columns = set(cm_df.columns)
cm_req_col = cm_columns.intersection(required_columns)
cm_req_df = cm_df[cm_req_col]

cm_req_df.SUBJID = ae_req_df.SUBJID

df = pd.join(ae_req_df, cm_req_df, on="SUBJID")
# %%

##  EDA
# Convert all dates to dates
def refactor_date(date_str):
    print(date_str)
    # if "00:00:00" in date_str:
    #     date_str = date_str.replace("00:00:00", "")
    #     return date_str
    # else:
    date = ""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        pass

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        pass


for col in df.columns:
    if 'DAT' in col:
        if str(df[col].dtype) == 'object':
            df[col].apply(lambda row: refactor_date)
        df[col] = pd.to_datetime(df[col])

# %%

# Functions
