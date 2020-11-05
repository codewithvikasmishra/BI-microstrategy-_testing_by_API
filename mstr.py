import requests
import json
import csv

base_url="microstartegy link for your products"
doc_id = 'document id of microstrategy document'
proj_id = 'project id of microstrategy document'
dossiers = 'dossier id of microstrategy document'
mstr_res=[]

# Logging in to microstrategy and also we need to capture the cookie so we can use that in our next API
def login():
    headers={'Content-Type':'application/json'}
    response=requests.post(base_url+'/MicroStrategyLibrary/api/auth/login',
    json={"username":"******","password":"*****","loginMode":1},headers = headers)
    cookie='JSESSIONID='+response.get_dict().get('JSESSIONID')+';'+'iSession='=+response.get_dict().get('iSession')
    return reponse.headers.get('X-MSTR-AuthToken'),cookie

# to get the mid (instance) of the project
def instance(inst):
    headers={'Content-Type':'application/json','X-MSTR-AuthToken':inst[0],'X-MSTR-ProjectID':proj_id,'cookie':inst[1]}
    res_inst=requests.post(base_url+'/MicroStrategyLibrary/api/documents/'+doc_id+'/instances',
    headers=headers)
    return res_inst.json().get('mid')

# to get the prompts within a microstrategy document
def prompt(inst,mid):
    headers={'Content-Type':'application/json','X-MSTR-AuthToken':inst[0],'X-MSTR-ProjectID':proj_id,'cookie':inst[1]}
    res_prompt=requests.post(base_url+'/MicroStrategyLibrary/api/documents/'+doc_id+'/instances'+mid+'/prompts',
    headers=headers)
    return res_prompt.json()

# to get the data in excel
def excel_export(inst,mid):
    headers={'Content-Type':'application/json','X-MSTR-AuthToken':inst[0],'X-MSTR-ProjectID':proj_id,'cookie':inst[1]}
    res_exp_xls=requests.post(base_url+'/MicroStrategyLibrary/api/documents/'+doc_id+'/instances'+mid+'/excel',headers=headers)
    return res_exp_xls.text

# to get the instance for the dossiers
def dossier_instance(inst,mid):
    headers={'Content-Type':'application/json','X-MSTR-AuthToken':inst[0],'X-MSTR-ProjectID':proj_id,'X-MSTR-AsyncMode':'true',
    'cookie':inst[1]}
    res_doss_inst=requests.post(base_url+'/MicroStrategyLibrary/api/dossiers/'+dossiers+'/instances',headers=headers)
    return reponse.json().get('mid')

# to get the visualization_key from microstrategy dossier and when dossier is in nested mode
def dossier_definition(inst):
    # visualization_key=[]
    headers={'Content-Type':'application/json','X-MSTR-AuthToken':inst[0],'X-MSTR-ProjectID':proj_id,'cookie':inst[1]}
    res_doss_def=requests.get(base_url+'/MicroStrategyLibrary/api/v2/dossiers/'+dossiers+'/definition',headers=headers)
    res=dict()
    for item in res_doss_def.json().get('chapters'):
        if isinstance(item, dict) and 'key' in item:
            res[item.get('key')]=[viz['key'] for page in item.get('pages') for viz in page.get('visualizations')]
    return res

# to get the numeric values from a microstartegy chapter
def chapter_visualization(inst,dossier_mid,chptr_key,viz_key):
    headers={'Content-Type':'application/json','X-MSTR-AuthToken':inst[0],'X-MSTR-ProjectID':proj_id,'cookie':inst[1]}
    res_chp_viz=requests.get(base_url+'/MicroStrategyLibrary/api/v2/dossiers/'+dossiers+'/instances/'
    +dossier_mid+'/chapters'+chptr_key+'/visualizations'+viz_key+'?limit=1000',headers=headers)
    mstr_res.append(response.json().get('data').get('metricValues').get('formatted'))
    return response.json().get('data').get('metricValues').get('formatted')

# to get the all numeric values for a chapter key and then moving into an excel file
inst=login()
mid=instance(inst)
dossier_mid=dossier_instance(mid)

d_def={}
d_def=dossier_definition(inst)

for key,value in d_def.items():
    if key=='************************':
        chptr_key=key
        for value in range(len(d_def.get('key'))):
            if d_def.get(key)[value]=='***********************'
            viz_key=d_def.get(key)[value]
            chapter_visualization(inst,dossier_mid,chptr_key,viz_key)
    else:
        pass

# writing the dat into excel file with new lines
with open('path_where_you_want_to_save\\MSTR_Res.csv',"w") as f:
    A=csv.writer(f,lineterminator="\n")
    A=writerows(mstr_res)