#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  TBV.py
#  
#  Copyright B. Díaz
#
############################################-1-################################

import pandas as pd
import numpy as np
import clean_functions as cl
import os
import sys

new_path = '/home/dsc/Repos/TFM-Test-your-business-viability/TBV_v1'

if new_path not in sys.path:
	sys.path.append(new_path)


def missing_id(df1,df2):
    arr1 = []
    arr2 = []
    missing_id_df1 = []
    missing_id_df2 = []
    
    df1.drop_duplicates()
    df2.drop_duplicates()
    
    arr1 = df1.id_local.unique()
    arr2 = df2.id_local.unique()
    missing_id_df1 = [x for x in arr1 if x not in arr2]
    missing_id_df2 = [x for x in arr2 if x not in arr1]
    
    return(missing_id_df1,missing_id_df2)

def id_situacion(df):
    df.loc[df['desc_situacion_local'] == 'Abierto','id_situacion_local'] = 1
    df.loc[df['desc_situacion_local'] == 'Cerrado','id_situacion_local'] = 4
    df.loc[df['desc_situacion_local'] == 'Uso vivienda','id_situacion_local'] = 5
    df.loc[df['desc_situacion_local'] == 'En obras','id_situacion_local'] = 7
    df.loc[df['desc_situacion_local'] == 'Baja','id_situacion_local'] = 8
    df.loc[df['desc_situacion_local'] == 'Baja Reunificacion','id_situacion_local'] = 9
    df.loc[df['desc_situacion_local'] == 'Baja PC Asociado','id_situacion_local'] = 10
    return df

def estado(column1, column2):
    if len(column1) != len(column2):
        return 'Error'
    conditions = [
        (column1 == 'LOCAL SIN ACTIVIDAD') & (column2 == 'Abierto'), 
        (column2 == 'Baja'),
        (column2 == 'Baja PC Asociado'),
        (column2 == 'Baja Reunificacion'),
        (column1 == 'LOCAL SIN ACTIVIDAD') & (column2 == 'En obras'),
        (column2 == 'Cerrado'),
        (column2 == 'Uso vivienda'),
        (column2 == 'Abierto'),
        (column2 == 'En obras')
        ]
    outputs = ['Cerrado','Cerrado','Cerrado','Cerrado','Cerrado',
               'Cerrado','Uso vivienda','Abierto','En obras']
    
    res = np.select(conditions,outputs,'Other')
    
    return res

def new_col(df):
    df['conc'] = df.rotulo.str.strip() + "-" + df.desc_vial_acceso.str.strip() + "-" + df.num_acceso.astype(str) 
    df['id_local_norm'] = df['id_local']
    return df


#función para unificar y normalizar id. También unficar la desc_sit_loc_modif

def clear_id(df1, df2): 
    
    arr1 = []
    arr2 = []
    arr3 = []
    arr4 = []
    equal_conc_1 = []
    equal_conc_2 = []
    
    columns_of_interest_rest=['id_local','desc_epigrafe','id_local_norm','conc','desc_situacion_local']
    
    print(columns_of_interest_rest)
    
    df2_ = pd.DataFrame(df2, columns=columns_of_interest_rest)
    
    print(df2_.info())
    
    df1.drop_duplicates()
    df2_.drop_duplicates()
    
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1,df2_)
    
    arr1 = df1[df1.id_local.isin(missing_id_df1_)].conc.unique()
    arr2 = df2_.conc.unique()
    equal_conc_1 = [x for x in arr1 if x in arr2]
    
    df1_ = df1.copy()
        
    for i in equal_conc_1:
        df1_.loc[df1_.conc == i,'id_local_norm'] = min(df1_.loc[df1_.conc == i,'id_local'].values)
        df2_.loc[df2_.conc == i,'id_local_norm'] = df1_.loc[df1_.conc == i,'id_local'].values[0]
    
    df1_.drop_duplicates(subset=['id_local','conc','desc_epigrafe'],keep='last',inplace=True)
    df2_.drop_duplicates(subset=['id_local','conc','desc_epigrafe'],keep='last',inplace=True)
    
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_,df2_)

    arr3 = df2_[df2_.id_local.isin(missing_id_df2_)].conc.unique()
    arr4 = df1_.conc.unique()
    
    equal_conc_2 = [x for x in arr3 if x in arr4]
    
    for i in equal_conc_2:
        df2_.loc[df2_.conc == i,'id_local_norm'] = max(df2_.loc[df2_.conc == i,'id_local'].values)
        df1_.loc[df1_.conc == i,'id_local_norm'] = df2_.loc[df2_.conc == i,'id_local'].values[0]
    
    df1_.drop_duplicates(subset=['id_local','conc','desc_epigrafe'],keep='last',inplace=True)
    df2_.drop_duplicates(subset=['id_local','conc','desc_epigrafe'],keep='last',inplace=True)
    
    # completo el fichero final con los ids missing del fichero del año anterior
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_,df2_)
    if len(missing_id_df2_) > 0:
        df_concat = df2_[df2_.id_local.isin(missing_id_df2_)]
        df_concat.desc_situacion_local = 'Cerrado'
    
    df1_final = pd.concat([df1_,df_concat],sort=False)
    
    #completo el 'id_situacion_local' vacio
    df1_final_ = cl.id_situacion(df1_final)
    
    #unifico estados
    df1_final_['desc_sit_loc_modif'] = cl.estado(df1_final_['desc_epigrafe'], df1_final_['desc_situacion_local'])

    
    return(df1_final_,df2_)


#función para tratar NAs

def na(df): 

#me quedo con las columnas que me interesan
    columns_of_interest_19 =['id_local', 'id_distrito_local', 'desc_distrito_local', 'id_barrio_local', 'desc_barrio_local', 
                             'coordenada_x_local', 'coordenada_y_local', 'desc_tipo_acceso_local','id_situacion_local', 
                             'desc_situacion_local', 'clase_vial_acceso', 'desc_vial_acceso', 'nom_acceso', 'num_acceso', 'cal_acceso', 
                             'coordenada_x_agrupacion', 'coordenada_y_agrup', 'id_agrupacion', 'nombre_agrupacion', 'id_tipo_agrup', 
                             'desc_tipo_agrup', 'rotulo', 'id_seccion', 'desc_seccion', 'id_division', 'desc_division', 'id_epigrafe', 
                             'desc_epigrafe','conc', 'id_local_norm','desc_sit_loc_modif']
    
    df = pd.DataFrame(df, columns=columns_of_interest_19)

#completo el 'id_situacion_local' vacio
    df_final = cl.id_situacion(df)
    
#trato los NaN
    df_final['id_seccion'].fillna('Z',inplace=True)
    df_final['desc_seccion'].fillna('SIN ACTIVIDAD',inplace=True)
    df_final['id_division'].fillna(0,inplace=True)
    df_final['desc_division'].fillna('SIN ACTIVIDAD',inplace=True)
    df_final['id_epigrafe'].fillna(0,inplace=True)
    df_final['desc_epigrafe'].fillna('LOCAL SIN ACTIVIDAD',inplace=True)
    df_final['nombre_agrupacion'].fillna('SIN AGRUPACION',inplace=True)
    df_final['desc_tipo_agrup'].fillna('SIN AGRUPACION',inplace=True)
    df_final['id_tipo_agrup'].fillna(-1,inplace=True)
    df_final['id_agrupacion'].fillna(-1,inplace=True)
    df_final['coordenada_x_agrupacion'].fillna(0,inplace=True)
    df_final['coordenada_y_agrup'].fillna(0,inplace=True)

    return(df_final)

def reset(df):
    df.sort_values(['id_local_norm'],inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

def unif_id(df1,df2):
    n = 0
    for i in df2.conc.values:
        if i in df1.conc.values:
            df1.loc[df1.conc == i,'id_local_norm'] = max(df1.loc[df1.conc== i,'id_local'].values)
            df2.loc[df2.conc == i,'id_local_norm'] = df1.loc[df1.conc == i,'id_local_norm']
    n += 1
    print(i,n)
    return(df1,df2)
