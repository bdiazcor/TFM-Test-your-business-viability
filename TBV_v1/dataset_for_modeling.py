#!/usr/bin/env python
# coding: utf-8

'''Script to load a prepare dataset of Commercial premises for modeling'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import importlib
from sklearn.model_selection import train_test_split

# Load DataFrame, #convert index to id_local 
df_locals = pd.read_csv('Data/censolocales/locals_sh_f_back.csv')
df_locals = df_locals.set_index(df_locals.id_local).drop('id_local',axis=1)

#Select the columns of interest and filter the DataFrame
columns_of_interest = ['id_distrito_local','id_barrio_local', 'id_epigrafe', 'target', 'id_tipo_agrup','ab_17_19', 
'loc_dist_act', 'ab_dist_act_17_19', 'total_loc_act', 'total_ab_act_17_19', 'loc_dist', 'ab_dist_17_19',
'loc_na_dist', 'ab_dist_act_17_19_rate', 'total_ab_act_17_19_rate', 'total_ab_dist_17_19_rate', 'total_na_dist_rate',
'loc_barrio_act', 'ab_barrio_act_17_19', 'loc_barrio', 'ab_barrio_17_19', 'loc_na_barrio', 'ab_barrio_act_17_19_rate',
'total_ab_barr_17_19_rate','total_na_barr_rate', 'lon', 'lat', 'num_act', 'Población', 'Hombre', 
'Mujeres', 'Densidad (Habitantes / Ha.)', 'Edad mediana', 'Renta media/persona (euros)', 'Total Hogares', 'Españoles', 'Extranjeros',
'España fuera barrio dia laboral', 'Extranjero fuera barrio dia laboral', 'Total fuera barrio dia laboral',
'España fuera barrio fin semana', 'Extranjero fuera barrio fin semana',
'Total fuera barrio fin semana', 'Total barrio dia laboral', 'Total barrio fin semana',
'Total trabajo dia laboral', 'Total trabajo fin semana', 'total_TF_week',
'ratio_t_total', 'ratio_fb_total', 'ratio_b_total', 'dist_type', 'points_in_radius']

df_locals_v2 = df_locals[columns_of_interest]

# After feature correlation check, I just keept 16 variables for modeling 
cols_drop = ['id_barrio_local', 'ab_barrio_act_17_19', 'loc_dist', 'loc_na_dist', 'loc_barrio', 
             'total_na_dist_rate', 'total_ab_act_17_19_rate','ab_dist_act_17_19', 'loc_dist_act',
             'Población', 'Hombre','Total Hogares',
             'Extranjeros', 'Españoles', 
             'España fuera barrio dia laboral', 'Extranjero fuera barrio dia laboral',
             'Total fuera barrio dia laboral', 'España fuera barrio fin semana',
             'Total fuera barrio fin semana',
             'Total barrio dia laboral', 'Total barrio fin semana',
             'Total trabajo dia laboral', 'total_TF_week',
             'ratio_t_total', 'ratio_fb_total', 'ratio_b_total']

df_locals_final = df_locals_v2.drop(cols_drop, axis=1)

# categorical and numerical features
cat_feature = ['id_distrito_local', 'id_epigrafe', 'id_tipo_agrup','dist_type','ab_17_19']
num_feature = ['total_loc_act', 'total_ab_act_17_19', 'ab_dist_17_19', 'ab_dist_act_17_19_rate', 
               'total_ab_dist_17_19_rate', 'loc_barrio_act', 'ab_barrio_17_19', 'loc_na_barrio', 
               'ab_barrio_act_17_19_rate', 'total_ab_barr_17_19_rate', 'total_na_barr_rate', 'lon', 
               'lat','num_act', 'Mujeres', 'Densidad (Habitantes / Ha.)', 'Edad mediana',
               'Renta media/persona (euros)', 'Extranjero fuera barrio fin semana',
               'Total trabajo fin semana','points_in_radius' ]

# dummify categorical variables
df_locals_final = pd.get_dummies(df_locals_final, columns = cat_feature)

# 5% subset for final validation (df_locals_reserved)
data_reserved = df_locals_final.sample(frac = 0.05,random_state=42)
print('Total sample reserved: %0.0f' %(len(data_reserved)))

# I generate X and y variables and training and test split with the remaining dataset.
df_locals_rest = df_locals_final.drop(data_reserved.index, axis = 0)
print('Total population before train and test split: %0.0f' %len(df_locals_rest))

X = df_locals_rest.drop('target',axis=1)
y = df_locals_rest['target']

# train and test split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)

print('X_train, y_train, X_test, y_test and data_reserved returned')



