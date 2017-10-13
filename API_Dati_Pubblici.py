
# coding: utf-8

# In[168]:

#import sys
#reload(sys)
#sys.setdefaultencoding("latin-1")


# # API dati.gov.it

# In[36]:

# import libraries
import pandas as pd
import numpy as np
import html
import datetime


# ## Lista dei Dataset Pubblicati sul sito dati.gov.it

# In[2]:

# Recupera la lista degli Open Data
url_list = 'http://www.dati.gov.it/api/3/action/package_list'
df_list = pd.read_json(url_list)
# Numero di dataset
df_list['result'].count()


# ## Dataset dei Metadati

# In[6]:

url_test = 'http://www.dati.gov.it/api/3/action/package_show?id='+df_list['result'][2]
df_meta = pd.read_json(url_test)
df_meta.head(2)


# In[29]:

def crea_df_metadato(df_name):
    url_meta = 'http://www.dati.gov.it/api/3/action/package_show?id='+df_name
    d = {}
    try:
        df_meta = pd.read_json(url_meta)
        d['ds_name']=df_name
        d['ds_title'] = df_meta['result']['title']
        d['ds_id'] = df_meta['result']['id']
        d['ds_license'] = df_meta['result']['license_id']
        d['_catalog_parent_name']=df_meta['result']['_catalog_parent_name']
        d['ultima_modifica']=html.unescape(df_meta['result']['extras'][1]['value'])
        d['gruppo'] = df_meta['result']['groups'][0]['display_name']
        d['note'] = df_meta['result']['notes']
        if 'resources' in df_meta['result']:
            d['url']=df_meta['result']['resources'][-1]['url']
            d['mymtype']=df_meta['result']['resources'][-1]['mimetype']
        else:
            d['url'] = np.nan
            d['mymtype'] = np.nan
    except:
        d['ds_name']=df_name
        d['ds_title'] = np.nan
        d['ds_id'] = np.nan
        d['ds_license'] = np.nan
        d['_catalog_parent_name']=np.nan
        d['ultima_modifica'] = np.nan
        d['gruppo'] = np.nan
        d['note'] = np.nan
        d['url'] = np.nan
        d['mymtype'] = np.nan
    return d


# In[30]:

def crea_df_metadati_all(df_list):
    l = []
    for index, row in df_list.iterrows():
        l.append(crea_df_metadato(row['result']))
    df = pd.DataFrame.from_dict(l)
    return df


# In[31]:

df_list_test = df_list[0:10]


# In[32]:

df = crea_df_metadati_all(df_list_test)
cols = ['ds_title','_catalog_parent_name','gruppo','note','ultima_modifica',
       'ds_name','ds_id','ds_license','url','mymtype']
df = df[cols]


# In[33]:

df.head(2)


# In[42]:

now = datetime.datetime.now()
dt = now.strftime("%Y-%m-%d")
name_file = dt+'_df_metadati_pa.csv'


# In[43]:

df.to_csv(path_or_buf=name_file, sep=';')


# ## Get Dataset from Url

# In[158]:

df = pd.read_csv(r['url'])


# In[159]:

df.head(2)

