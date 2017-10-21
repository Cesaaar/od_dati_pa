# import libraries
import pandas as pd
import numpy as np
import HTMLParser
import datetime
import luigi
import os

class DsMetadatiPA(luigi.Task):
    
    def output(self):
        now = datetime.datetime.now()
        dt = now.strftime("%Y-%m-%d")
        filename = dt + '_DSMetadatiPA.csv'
		dir_in = os.path.join(os.path.abspath(''),'input')
		df_file = os.path.join(dir_in, filename)
        return luigi.LocalTarget(df_file)
    
    def run(self):
        
        # Recupera la lista degli Open Data
        url_list = 'http://www.dati.gov.it/api/3/action/package_list'
        df_list = pd.read_json(url_list)
        
        df_list = df_list[0:20]
        
        count = df_list['result'].count()
        
        l = []
        i = 1
        for index, row in df_list.iterrows():
            progress = i*100/count
            self.set_status_message("Progress Bar")
            url_meta = 'http://www.dati.gov.it/api/3/action/package_show?id='+row['result']
            d = {}
            try:
                df_meta = pd.read_json(url_meta)
                d['ds_name']=row['result']
                d['ds_title'] = df_meta['result']['title']
		d['ds_id'] = df_meta['result']['id']
                d['_catalog_parent_name']=df_meta['result']['_catalog_parent_name']
		try:
			d['ds_license'] = df_meta['result']['license_id']
		except:
			d['ds_license'] = np.nan
                try:
			 d['ultima_modifica']=df_meta['result']['metadata_modified'][0:10]
                except:
                    	d['ultima_modifica']=np.nan
		try:
			d['gruppo'] = df_meta['result']['groups'][0]['display_name']
		except:
			d['gruppo'] = np.nan
		try:
			d['note'] = df_meta['result']['notes']
		except:
			d['note'] = np.nan
		try:
			d['url']=df_meta['result']['resources'][-1]['url']
			d['mymtype']=df_meta['result']['resources'][-1]['mimetype']
		except:
			d['url'] = np.nan
			d['mymtype'] = np.nan
            except:
                d['ds_name']=row['result']
                d['ds_title'] = np.nan
                d['ds_id'] = np.nan
                d['ds_license'] = np.nan
                d['_catalog_parent_name']=np.nan
                d['ultima_modifica'] = np.nan
                d['gruppo'] = np.nan
                d['note'] = np.nan
                d['url'] = np.nan
                d['mymtype'] = np.nan
            self.set_progress_percentage(progress)
            l.append(d)
            i=i+1

        df = pd.DataFrame.from_dict(l)
        cols = ['ds_title','_catalog_parent_name','gruppo','note','ultima_modifica',
                    'ds_name','ds_id','ds_license','url','mymtype']
        df = df[cols]

        df.to_csv(path_or_buf=self.output().path, sep=';', encoding='utf-8')
