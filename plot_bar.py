import json
import matplotlib.pyplot as plt
import pandas as pd

metadata_path = '/home/budi/indonesian_government/apps_screening/province_metadata.csv'
app_prov_path = '/home/budi/indonesian_government/apps_screening/province_source.csv'
prov_list_path = '/home/budi/indonesian_government/apps_screening/province_list.csv'

data_df = pd.read_csv(metadata_path)#,sep=';')
# print(data_df[['appId','rating','score','review','install']])

source_df = pd.read_csv(app_prov_path)#,sep=';')
# print(source_df)

data_source_df = pd.merge(data_df,source_df,left_on='appId',right_on='app_id',how='inner')
data_source_df=data_source_df.fillna(0)
# print(data_source_df)
data_source_df['install']=data_source_df['install'].replace('error',0).astype(float)
data_source_df['review']=data_source_df['review'].replace('error',0).astype(float)
data_source_df['score']=data_source_df['score'].replace('error',0).astype(float)
new_df = data_source_df.groupby(['province'])['province'].count().reset_index(name='app_number').sort_values(by=['app_number'],ascending=False)
avg_install_df = data_source_df.groupby(['province'])['install'].mean().reset_index()
avg_review_df = data_source_df.groupby(['province'])['review'].mean().reset_index()
avg_score_df = data_source_df.groupby(['province'])['score'].mean().reset_index()
new_df=pd.merge(new_df,avg_install_df,left_on='province',right_on='province',how='inner')
new_df=pd.merge(new_df,avg_review_df,left_on='province',right_on='province',how='inner')
new_df=pd.merge(new_df,avg_score_df,left_on='province',right_on='province',how='inner')
# print(new_df)
# merge to all province including province without apps
prov_list = pd.read_csv(prov_list_path)
new_df=pd.merge(prov_list,new_df,left_on='province_name',right_on='province',how='left')
new_df=new_df.fillna(0).sort_values(by=['app_number'])
print(new_df)

# print(new_df)

parameter = new_df['province_name']
count = new_df['app_number']
fig = plt.figure(figsize=(8,6))
plt.xticks(rotation='vertical',fontsize=12)
plt.barh(parameter, count)
plt.ylabel('Province Name',fontsize=12)
plt.xlabel('Number of Apps',fontsize=12)
plt.tight_layout()
# fig.savefig(write_path)
plt.show()


# prov_df = pd.merge(prov_df,new_df,left_on='NAME_1',right_on='province',how='left')
# prov_df=prov_df.fillna(0)
# prov_df['inst_norm']=(prov_df['install']-prov_df['install'].min())/(prov_df['install'].max()-prov_df['install'].min())
# prov_df['rev_norm']=(prov_df['review']-prov_df['review'].min())/(prov_df['review'].max()-prov_df['review'].min())
# prov_df['sco_norm']=(prov_df['score']-prov_df['score'].min())/(prov_df['score'].max()-prov_df['score'].min())
# prov_df['popular'] = (prov_df['inst_norm']+prov_df['rev_norm']+prov_df['sco_norm'])/3
# print(prov_df)


