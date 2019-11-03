import pandas as pd
import numpy as np
import clean_functions as cl
import os
import sys

#función que compara dos dataframes y devuelve dos arrays de los id_local que aparecen en un dataframe y no en el otro y viceversa
def missing_id(df1,df2):
    arr1 = []
    arr2 = []
    missing_id_df1 = []
    missing_id_df2 = []
    
    df1.drop_duplicates()
    df2.drop_duplicates()
    
    arr1 = df1.id_local_norm.unique()
    arr2 = df2.id_local_norm.unique()
    missing_id_df1 = [x for x in arr1 if x not in arr2]
    missing_id_df2 = [x for x in arr2 if x not in arr1]
    
    return(missing_id_df1,missing_id_df2)

# funcion que incluye el id_situacion en dataframes (era un campo vacío en fichero de epigrafes) 
def id_sit(df):
    df.loc[df['desc_situacion_local'] == 'Abierto','id_situacion_local'] = int(1)
    df.loc[df['desc_situacion_local'] == 'Cerrado','id_situacion_local'] = int(4)
    df.loc[df['desc_situacion_local'] == 'Uso vivienda','id_situacion_local'] = int(5)
    df.loc[df['desc_situacion_local'] == 'En obras','id_situacion_local'] = int(7)
    df.loc[df['desc_situacion_local'] == 'Baja','id_situacion_local'] = int(8)
    df.loc[df['desc_situacion_local'] == 'Baja Reunificacion','id_situacion_local'] = int(9)
    df.loc[df['desc_situacion_local'] == 'Baja PC Asociado','id_situacion_local'] = int(10)
    return df

# función que normaliza el estado del local creando una nueva columna(desc_sit_loc_modif) en función de desc_epigrafe y 
# desc_situacion_local
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

#función que genera dos nuevas columnas de trabajo: 'conc': concatena rótulo con dirección e 'id_local_norm' para poder
#normalizar ids sin modificar la columna original
def new_col(df):
    df['conc'] = df.rotulo.str.strip() + "-" + df.desc_vial_acceso.str.strip() + "-" + df.num_acceso.astype(str) 
    df['id_local_norm'] = df['id_local']
    return df


#funcion para tratar NAs del fichero último año
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
    df_final = cl.id_sit(df)
    
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

# Funcion para quedarme con las columnas de interes de los dataframes del resto de años con los que voy a comparar
def col_rest(df): 
    columns_of_interest_rest=['id_local_norm','conc','desc_sit_loc_modif']
    df_d = pd.DataFrame(df, columns=columns_of_interest_rest)
    return df_d

# ordeno por id_local_norm y reseteo el indice
def reset(df):
    df.sort_values(['id_local_norm'],inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

# funcion que requiere mucho rendimiento. Compara una a una las diferencias entre los id_locales de dataframes y las
# unifica
def unif_id(df1,df2):
    n = 0
    for i in df2.conc.values:
        if i in df1.conc.values:
            df1.loc[df1.conc == i,'id_local_norm'] = max(df1.loc[df1.conc== i,'id_local'].values)
            df2.loc[df2.conc == i,'id_local_norm'] = df1.loc[df1.conc == i,'id_local_norm']
    n += 1
    print(i,n)
    return(df1,df2)

