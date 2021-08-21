import geopandas as gpd
import json
import matplotlib.pyplot as plt
import pandas as pd

geo_path = '/home/budi/indonesian_government/indonesian_province_geospatial/prov.geojson'
metadata_path = '/home/budi/indonesian_government/apps_screening/province_metadata.csv'
app_prov_path = '/home/budi/indonesian_government/apps_screening/province_source.csv'
write_path = '/home/budi/indonesian_government/analysis_result.csv'

prov_df = gpd.read_file(geo_path)
# prov_df['NAME_1'] = prov_df['NAME_1'].astype(str)

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
prov_df = pd.merge(prov_df,new_df,left_on='NAME_1',right_on='province',how='left')
prov_df=prov_df.fillna(0)
prov_df['inst_norm']=(prov_df['install']-prov_df['install'].min())/(prov_df['install'].max()-prov_df['install'].min())
prov_df['rev_norm']=(prov_df['review']-prov_df['review'].min())/(prov_df['review'].max()-prov_df['review'].min())
prov_df['sco_norm']=(prov_df['score']-prov_df['score'].min())/(prov_df['score'].max()-prov_df['score'].min())
prov_df['popular'] = (prov_df['inst_norm']+prov_df['rev_norm']+prov_df['sco_norm'])/3
print(prov_df)

prov_df.to_csv(write_path)

# set a variable that will call whatever column we want to visualise on the map
values = 'popular'
# set the value range for the choropleth
vmin = prov_df['popular'].min()  
vmax = prov_df['popular'].max() 
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(30, 10))
# remove the axis
ax.axis('off')
# add a title
# title = 'School Participations Rate for Age {}'.format(values)
# ax.set_title(title, fontdict={'fontsize': '25', 'fontweight' : '3'})
# create an annotation for the data source
# ax.annotate('Source: Badan Pusat Statistik Indonesia',
#     xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', 
#     verticalalignment='top', fontsize=12 ,color='#555555')
# Create colorbar as a legend
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin*100, vmax=vmax*100))
# add the colorbar to the figurec
# bar = fig.colorbar(sm,shrink=0.7, aspect=20*0.7)
# create map
prov_df.plot(column=values, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.7',norm=plt.Normalize(vmin=vmin, vmax=vmax))

prov_df['coords'] = prov_df['geometry'].apply(lambda x: x.representative_point().coords[:])
prov_df['coords'] = [coords[0] for coords in prov_df['coords']]
for idx, row in prov_df.iterrows():
    app = int(row['app_number'])
    pop = int(round(row['popular']*100,0))
    plt.annotate(s=str(pop)+'('+str(app)+')', xy=row['coords'],horizontalalignment='center',fontsize=8)
plt.show()