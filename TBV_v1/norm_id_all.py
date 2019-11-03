import pandas as pd
import numpy as np
import clean_functions as cl
import os
import sys

#función para unificar y normalizar id entre dos dataframes. El más reciente es el df1 y el menos reciente en df2.

def norm_id(df1, df2): 
    
    arr1 = []
    arr2 = []
    arr3 = []
    arr4 = []
    equal_conc_1 = []
    equal_conc_2 = []
    
    df2_d = df2.copy()
    df1_d = df1.copy()
    
    df1_d.drop_duplicates()
    df2_d.drop_duplicates()
    
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
    
    arr1 = df1_d[df1_d.id_local_norm.isin(missing_id_df1_)].conc.unique()
    arr2 = df2_d.conc.unique()
    equal_conc_1 = [x for x in arr1 if x in arr2]
    
    reset(df1_d)
    reset(df2_d)
    
    for i in equal_conc_1:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
    
    df1_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    df2_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    
    
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
    
    arr3 = df1_d[df1_d.id_local_norm.isin(missing_id_df1_)].conc.unique()
    arr4 = df2_d.conc.unique()
    equal_conc_2 = [x for x in arr3 if x in arr4]
        
    for i in equal_conc_2:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
    
    df1_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    df2_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    
    
    # completo el fichero final con los ids missing del fichero del año anterior
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
    
    if len(missing_id_df2_) > 0:
        df_concat = df2_d[df2_d.id_local_norm.isin(missing_id_df2_)]
        df_concat.desc_situacion_local = 'Cerrado'
    
    df1_final = pd.concat([df1_d,df_concat],sort=False)
        
    return(df1_final,df2_d)

# Función que compara el segundo años con el tercero tras haberlo normalizado con un segundo. No funciona bien
def norm_id_second(df1, df2): 
    
    arr1 = []
    arr2 = []
    arr3 = []
    arr4 = []
    equal_conc_1 = []
    equal_conc_2 = []
    
    df2_d = df2.copy()
    df1_d = df1.copy()
    
    df1_d.drop_duplicates()
    df2_d.drop_duplicates()
    
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
    
    arr1 = df1_d[df1_d.id_local_norm.isin(missing_id_df1_)].conc.unique()
    arr2 = df2_d.conc.unique()
    equal_conc_1 = [x for x in arr1 if x in arr2]
    
    reset(df1_d)
    reset(df2_d)
    
    for i in equal_conc_1:
#df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
    
    df1_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    df2_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    
    
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
    
    arr3 = df2_d[df2_d.id_local_norm.isin(missing_id_df2_)].conc.unique()
    arr4 = df1_d.conc.unique()
    equal_conc_2 = [x for x in arr3 if x in arr4]
        
    for i in equal_conc_2:
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
          
# completo el fichero final con los ids missing del fichero del año anterior
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
    
    if len(missing_id_df2_) > 0:
        df_concat = df2_d[df2_d.id_local_norm.isin(missing_id_df2_)]
        df_concat.desc_situacion_local = 'Cerrado'
    
    df1_final = pd.concat([df1_d,df_concat],sort=False)
        
    return(df1_final,df2_d)




#función que compara id de ficheros de 5 años y los unifica

def norm_id_all(df1, df2, df3, df4, df5): 
    
    arr1 = []
    arr2 = []
    arr3 = []
    arr4 = []
    arr5 = []
    arr6 = []
    arr7 = []
    arr8 = []
    arr9 = []
    arr10 = []
    arr11 = []
    arr12 = []
    arr13 = []
    arr14 = []
    arr15 = []
    arr16 = []
    
    equal_conc_1 = []
    equal_conc_2 = []
    equal_conc_3 = []
    equal_conc_4 = []
    equal_conc_5 = []
    equal_conc_6 = []
    equal_conc_7 = []
    equal_conc_8 = []
                
    df1_d = df1.copy()
    df2_d = df2.copy()
    df3_d = df3.copy()
    df4_d = df4.copy()
    df5_d = df5.copy()
    
    df1_d.drop_duplicates()
    df2_d.drop_duplicates()
    df3_d.drop_duplicates()
    df4_d.drop_duplicates()
    df5_d.drop_duplicates()
    
#los ordeno por id_local_norm
    reset(df1_d)
    reset(df2_d)
    reset(df3_d)
    reset(df4_d)
    reset(df5_d)
    
#missing ids con respecto el fichero final
#lo voy calculando dos a dos: uĺtimo año con penúltimo
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
    
    arr1 = df1_d[df1_d.id_local_norm.isin(missing_id_df1_)].conc.unique()
    arr2 = df2_d.conc.unique()
    
    equal_conc_1 = [x for x in arr1 if x in arr2]
        
    for i in equal_conc_1:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df3_d.loc[df3_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df4_d.loc[df4_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df5_d.loc[df5_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
    
#ahora miro si hay alguna diferencia con respecto a al antepenúltimo
    missing_id_df1_, missing_id_df3_ = cl.missing_id(df1_d,df3_d)
    
    arr3 = df1_d[df1_d.id_local_norm.isin(missing_id_df1_)].conc.unique()
    arr4 = df3_d.conc.unique()
    
    equal_conc_2 = [x for x in arr3 if x in arr4]
        
    for i in equal_conc_2:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df3_d.loc[df3_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df4_d.loc[df4_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df5_d.loc[df5_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)        

#ahora miro si hay alguna diferencia con respecto a hace 4 años
    missing_id_df1_, missing_id_df4_ = cl.missing_id(df1_d,df4_d)
    
    arr5 = df1_d[df1_d.id_local_norm.isin(missing_id_df1_)].conc.unique()
    arr6 = df4_d.conc.unique()
    
    equal_conc_3 = [x for x in arr5 if x in arr6]
        
    for i in equal_conc_3:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df3_d.loc[df3_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df4_d.loc[df4_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df5_d.loc[df5_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
    
#ahora miro si hay alguna diferencia con respecto a hace cinco antes
    missing_id_df1_, missing_id_df5_ = cl.missing_id(df1_d,df5_d)
    
    arr7 = df1_d[df1_d.id_local_norm.isin(missing_id_df1_)].conc.unique()
    arr8 = df5_d.conc.unique()
    
    equal_conc_4 = [x for x in arr7 if x in arr8]
        
    for i in equal_conc_4:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df3_d.loc[df3_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df4_d.loc[df4_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df5_d.loc[df5_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
    
    
#ahora lo hago al revés: anterior con actual
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
    
    arr9 = df2_d[df2_d.id_local_norm.isin(missing_id_df2_)].conc.unique()
    arr10 = df1_d.conc.unique()
    equal_conc_5 = [x for x in arr9 if x in arr10]
        
    for i in equal_conc_5:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df3_d.loc[df3_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df4_d.loc[df4_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df5_d.loc[df5_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)    
    
#ahora lo hago al revés: antepenultimo con actual
    missing_id_df1_, missing_id_df3_ = cl.missing_id(df1_d,df3_d)
    
    arr11 = df3_d[df3_d.id_local_norm.isin(missing_id_df3_)].conc.unique()
    arr12 = df1_d.conc.unique()
    equal_conc_6 = [x for x in arr11 if x in arr12]
        
    for i in equal_conc_6:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df3_d.loc[df3_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df4_d.loc[df4_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df5_d.loc[df5_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)    
    
#ahora lo hago al revés: hace 4 años con actual
    missing_id_df1_, missing_id_df4_ = cl.missing_id(df1_d,df4_d)
    
    arr13 = df4_d[df4_d.id_local_norm.isin(missing_id_df4_)].conc.unique()
    arr14 = df1_d.conc.unique()
    equal_conc_7 = [x for x in arr13 if x in arr14]
        
    for i in equal_conc_7:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df3_d.loc[df3_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df4_d.loc[df4_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df5_d.loc[df5_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)  
    
#ahora lo hago al revés: hace 5 años con actual
    missing_id_df1_, missing_id_df5_ = cl.missing_id(df1_d,df5_d)
    
    arr15 = df5_d[df5_d.id_local_norm.isin(missing_id_df5_)].conc.unique()
    arr16 = df1_d.conc.unique()
    equal_conc_8 = [x for x in arr15 if x in arr16]
        
    for i in equal_conc_8:
        df1_d.loc[df1_d.conc == i,'id_local_norm'] = max(df1.loc[df1.conc == i,'id_local_norm'].values)
        df2_d.loc[df2_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df3_d.loc[df3_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df4_d.loc[df4_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
        df5_d.loc[df5_d.conc == i,'id_local_norm'] = max(df1_d.loc[df1_d.conc == i,'id_local_norm'].values)
    
# compruebo si quedan aún algunos ids missing de años anteriores y concateno: primero anterior
    missing_id_df1_, missing_id_df2_ = cl.missing_id(df1_d,df2_d)
        
    if len(missing_id_df2_) > 0:
        df_concat1 = df2_d[df2_d.id_local_norm.isin(missing_id_df2_)]
        df_concat1.desc_situacion_local = 'Cerrado'
    
    df1_fin1 = pd.concat([df1_d,df_concat1],sort=False)
    
# compruebo si quedan aún algunos ids missing de años anteriores y concateno: antepenultimo
    missing_id_df1_, missing_id_df3_ = cl.missing_id(df1_fin1,df3_d)
    if len(missing_id_df3_) > 0:
        df_concat2 = df3_d[df3_d.id_local_norm.isin(missing_id_df3_)]
        df_concat2.desc_situacion_local = 'Cerrado'
    
    df1_fin2 = pd.concat([df1_fin1,df_concat2],sort=False)
    
# compruebo si quedan aún algunos ids missing de años anteriores y concateno: cuatro años antes
    missing_id_df1_, missing_id_df4_ = cl.missing_id(df1_fin2,df4_d)
    if len(missing_id_df4_) > 0:
        df_concat3 = df4_d[df4_d.id_local_norm.isin(missing_id_df4_)]
        df_concat3.desc_situacion_local = 'Cerrado'
    
    df1_fin3 = pd.concat([df1_fin2,df_concat3],sort=False)
    
# compruebo si quedan aún algunos ids missing de años anteriores y concateno: cinco años antes
    missing_id_df1_, missing_id_df5_ = cl.missing_id(df1_fin3,df5_d)
    if len(missing_id_df5_) > 0:
        df_concat4 = df5_d[df5_d.id_local_norm.isin(missing_id_df5_)]
        df_concat4.desc_situacion_local = 'Cerrado'
    
    df1_final = pd.concat([df1_fin3,df_concat4],sort=False)
    
    df1_final.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    df2_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    df3_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    df4_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    df5_d.drop_duplicates(subset=['id_local_norm','conc','desc_epigrafe'],keep='last',inplace=True)
    
    return(df1_final,df2_d,df3_d,df4_d,df5_d)
