#%%
import requests
import pandas as pd
from datetime import datetime
# %%

subject_list_url = 'https://pyhack-dot-pharmanlp-177020.uc.r.appspot.com/api/1/StudyHack/{}/subject/list'
subject_data_list_url = 'https://pyhack-dot-pharmanlp-177020.uc.r.appspot.com/api/1/StudyHack/{}/subject/{}/list'
query_url = 'https://pyhack-dot-pharmanlp-177020.uc.r.appspot.com/api/1/StudyHack/query'

for domain in domain_ids:
    url = subject_list_url.format(domain)


def get_all_subject_response(domain):
    url = subject_list_url.format(domain)
    response = requests.get(url)
    return response.json()

def get_subject_list(domain):
    response = get_all_subject_response(domain)
    data = response['data']
    return data


ae_subject_list = set(get_subject_list('ae'))
cm_subject_list = set(get_subject_list('cm'))
# %%

common_subject_list = list(ae_subject_list.intersection(cm_subject_list))
ae_required_columns = ['aeterm', 'aestdat', 'aespid', 'aeendat', 'aetoxgr', 'aecm', 'subjid', 'subjectid', 'siteid', "formname", "formid", "formidx"]
cm_required_columns = ['cmtrt', 'cmstdat', 'cmendat', 'cmaeno', 'subjid', 'siteid']
ae_df = pd.DataFrame()
cm_df = pd.DataFrame()

ae_req_df = pd.DataFrame(columns=ae_required_columns)
cm_req_df = pd.DataFrame(columns=cm_required_columns)


def get_subject_data_response(domain, subject):
    url = subject_data_list_url.format(domain, subject)
    response = requests.get(url)
    return response.json()

def get_subject_data_list(domain, subject):
    response = get_subject_data_response(domain, subject)
    data = response['data']
    return data

for subject_id in common_subject_list:
    ae_subject_data_list = get_subject_data_list('ae', subject_id)
    cm_subject_data_list = get_subject_data_list('cm', subject_id)
    ae_df = pd.DataFrame(ae_subject_data_list, columns=ae_required_columns)
    cm_df = pd.DataFrame(cm_subject_data_list, columns=cm_required_columns)

    ae_columns = set(ae_df.columns)
    ae_req_col = ae_columns.intersection(ae_required_columns)
    ae_req_df = ae_req_df.append(ae_df[ae_req_col]).reset_index(drop=True)

    cm_columns = set(cm_df.columns)
    cm_req_col = cm_columns.intersection(cm_required_columns)
    cm_req_df = cm_req_df.append(cm_df[cm_req_col]).reset_index(drop=True)

df = ae_req_df.join(cm_req_df.set_index('subjid'), 'subjid', how='left', rsuffix="cm")

# %%

custom_months = {
    50: "/01",
    51: "/02",
    52: "/03",
    53: "/04",
    54: "/05",
    55: "/06",
    56: "/07",
    57: "/08",
    58: "/09",
    59: "/10",
    60: "/11",
    61: "/12",
}
def refactor_date(date_str):
    date = ""
    for month in custom_months:
        replace_str = "/{}".format(month)
        if replace_str in date_str:
            date_str = date_str.replace(replace_str, custom_months[month])
    try:
        date = datetime.strptime(date_str, "%d-%b-%y")
        return date
    except:
        pass

    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")
        return date
    except:
        pass
    return date


for col in df.columns:
    if 'dat' in col:
        df[col] = df[col].apply(lambda row: refactor_date(row))
        df[col] = pd.to_datetime(df[col])

# %%
# Type 1

type1_df = df[df.aestdat < df.cmstdat]
type1_df["type"] = "TYPE1"
type1_df["email_address"] = "joelhanson2511995@gmail.com"
type1_dict = type1_df[["formname", "formid", "formidx", 'type', 'subjectid', 'email_address']].to_dict(orient='record')


# %%

# Type 2

type2_df = df[df.cmstdat < df.aeendat]
type2_df["type"] = "TYPE2"
type2_df["email_address"] = "joelhanson2511995@gmail.com"
type2_dict = type2_df[["formname", "formid", "formidx", 'type', 'subjectid', 'email_address']].to_dict(orient='record')

# %%

# Type 3

type3_df = df[(df.aeterm == df.aeterm) & (df.aestdat == df.aeendat)]
type3_df["type"] = "TYPE3"
type3_df["email_address"] = "joelhanson2511995@gmail.com"
type3_dict = type3_df[["formname", "formid", "formidx", 'type', 'subjectid', 'email_address']].to_dict(orient='record')

# %%

# Type 4
type4_df = df[(df.cmtrt == df.cmtrt) & (df.cmstdat == df.cmendat)]
type4_df["type"] = "TYPE4"
type4_df["email_address"] = "joelhanson2511995@gmail.com"
type4_dict = type4_df[["formname", "formid", "formidx", 'type', 'subjectid', 'email_address']].to_dict(orient='record')

# %%

# Type 
type5_df = df[~df.aeendat.isna() & ~df.cmendat.isna()]
type5_df["type"] = "TYPE5"
type5_df["email_address"] = "joelhanson2511995@gmail.com"
type5_dict = type5_df[["formname", "formid", "formidx", 'type', 'subjectid', 'email_address']].to_dict(orient='record')

# %%

def submit_query(query_list):
    response_data = []
    for query in query_list:
        response = request.post(query_url, data=query)
        response_data += response.json()
    return response_data

submit_query(type1_dict)
