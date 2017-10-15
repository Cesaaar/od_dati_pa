# import libraries
import pandas as pd
import numpy as np
import HTMLParser
import datetime
import luigi

class DsMetadatiPA(luigi.Task):
    
    def output(self):
        now = datetime.datetime.now()
        dt = now.strftime("%Y-%m-%d")
        filename = dt + '_DSMetadatiPA.csv'
        return luigi.LocalTarget(filename)
    
    def run(self):
        
        # Recupera la lista degli Open Data
        url_list = 'http://www.dati.gov.it/api/3/action/package_list'
        df_list = pd.read_json(url_list)
        
        #df_list_test = df_list[0:10]
        
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
                d['ds_license'] = df_meta['result']['license_id']
                d['_catalog_parent_name']=df_meta['result']['_catalog_parent_name']
                d['ultima_modifica']=HTMLParser.HTMLParser().unescape(df_meta['result']['extras'][1]['value'])
                d['gruppo'] = df_meta['result']['groups'][0]['display_name']
                d['note'] = df_meta['result']['notes']
                if 'resources' in df_meta['result']:
                    d['url']=df_meta['result']['resources'][-1]['url']
                    d['mymtype']=df_meta['result']['resources'][-1]['mimetype']
                else:
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
