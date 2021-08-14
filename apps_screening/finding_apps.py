"""
   Crawling apps metadata containing a certain keywords
   parsing parameter to metadata_scraper.js
"""

import time 
import os
import json
import pandas as pd
import csv


npm_path = '/home/budi/indonesian_government/apps_screening'
scrap_path = '/home/budi/indonesian_government/apps_screening/scrap_result/'
metadata_path = '/home/budi/indonesian_government/apps_screening/'
list_path = '/home/budi/indonesian_government/apps_screening/'

def scrap_by_keyword(result_path,npm_path,keyword):
    print ('Scrapping Apps Metadata using keyword :'+keyword)
    keyword = '"'+keyword+'"'
    # file_path = result_path+keyword
    # print(result_path)
    os.chdir(npm_path)
    os.system('node metadata_scraper '+keyword+' '+result_path)

def check_existing_result(result_path,keyword_list):
    existing_list = []
    new_list=[]
    for roots,dirs,files in os.walk(result_path):
        for file in files:
            check_file = (file.strip('.txt'))
            existing_list.append(check_file)
    for item in keyword_list:
        if item not in existing_list:
            new_list.append(item)
    return new_list

def encode_metadata(res_path):
    """Read JSON reasult from the scrape result folder"""
    for roots,dirs,files in os.walk(res_path):
        item_dict=[]
        for file in files:
            gov_id = file.replace('.txt','')
            # print(gov_id)
            try:
                file_path = roots+'/'+file
                # print(file_path)
                with open(file_path,'r') as app_metadata:
                    data=app_metadata.read()
                    json_data = json.loads(data)
                    for item in json_data:
                        app_id = item['appId'] if 'appId' in item else None
                        app_title = item['title'] if 'title' in item else None
                        developer = item['developer'] if 'developer' in item else None
                        summary = item['summary'] if 'summary' in item else None

                        item = {'appId':app_id, 'title':app_title,'gov_name':gov_id,'summary':summary,'developer':developer}
                        # print(item)
                        item_dict.append(item)
                        # item_dict.append({'appId':app_id, 'title':app_title,'description':description.strip('\n')})

            except IOError:
                print(IOError)

    return item_dict

def make_list (list_path):
    return_list =[]
    with open(list_path,'r') as fl:
        for item in fl:
            return_list.append(item.strip())
    return return_list

def main():

    # res_path = '/home/budi/indonesian_government/apps_screening/scrap_result/province'
    # key = 'pemerintah provinsi papua barat'
    # scrap_by_keyword(res_path,npm_path,key)

    metadata_list=[]
    gov_type=['province','district']
    for item in gov_type:
        res_path = scrap_path+item
        file_path = list_path+item+'_list.csv'

        keywords = make_list(file_path)
        # print(keyword)
        new_list = check_existing_result(res_path,keywords)
        for key in new_list:
            scrap_by_keyword(res_path,npm_path,key)
            print(key)
            time.sleep(1)

        
        meta_res = encode_metadata(res_path)
        for meta in meta_res:
            if item not in metadata_list:
                metadata_list.append(meta)

        mtdt_path = metadata_path+item+'_metadata.csv'
        metadata_df = pd.DataFrame(metadata_list)
        print(metadata_df)
        metadata_df.to_csv(mtdt_path)


if __name__=='__main__':
    main()
