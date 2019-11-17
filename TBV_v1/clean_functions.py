import pandas as pd
import numpy as np
import clean_functions as cl
import os
import sys
from geopy.distance import geodesic

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

#función que genera una nueva columnas de trabajo: 'conc': concatena rótulo con dirección e 'id_local_norm' para poder
def new_col(df):
    df['conc'] = df.rotulo.str.strip() + "-" + df.desc_vial_acceso.str.strip() + "-" + df.num_acceso.astype(str) 
    return df

#funcion para tratar NAs del fichero último año
def na(df): 
#me quedo con las columnas que me interesan
    columns_of_interest_19 =['id_local', 'id_distrito_local', 'desc_distrito_local', 'id_barrio_local', 'desc_barrio_local', 
                             'coordenada_x_local', 'coordenada_y_local', 'desc_tipo_acceso_local','id_situacion_local', 
                             'desc_situacion_local', 'clase_vial_acceso', 'desc_vial_acceso', 'nom_acceso', 'num_acceso', 'cal_acceso', 
                             'coordenada_x_agrupacion', 'coordenada_y_agrup', 'id_agrupacion', 'nombre_agrupacion', 'id_tipo_agrup', 
                             'desc_tipo_agrup', 'rotulo', 'id_seccion', 'desc_seccion', 'id_division', 'desc_division', 'id_epigrafe', 
                             'desc_epigrafe','conc', 'desc_sit_loc_modif']
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
    columns_of_interest_rest=['id_local','conc','desc_sit_loc_modif']
    df_d = pd.DataFrame(df, columns=columns_of_interest_rest)
    return df_d

# ordeno por id_local y reseteo el indice
def reset(df):
    df.sort_values(['id_local'],inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

#function to calculate the target variable based on the time a local has been opened (n years), starting the analysis since year m (2016-2018): 'cerrado_yy' == 1 & 'abierto_(yy-n)' == 1  -> target == 1
def target(df,n,year_i):
    
    df_ = df.copy()
    print(n)
    print(year_i)
    
    if n == 1: 
        if year_i == 2018:
            cond1 = (df_.cerrado_19 == 1) & (df_.abierto_18 == 1)                                  
        
            df_['target'] = np.where(cond1, 1 ,0)
    
        elif year_i == 2017:
            cond1 = (df_.cerrado_19 == 1) & (df_.abierto_18 == 1)
            cond2 = (df_.cerrado_18 == 1) & (df_.abierto_17 == 1)
        
            df_['target'] = np.where(cond1 | cond2, 1 ,0)   
        
        elif year_i == 2016:
            cond1 = (df_.cerrado_19 == 1) & (df_.abierto_18 == 1)
            cond2 = (df_.cerrado_18 == 1) & (df_.abierto_17 == 1)
            cond3 = (df_.cerrado_17 == 1) & (df_.abierto_16 == 1)
        
            df_['target'] = np.where((cond1 | cond2 | cond3), 1 ,0)
        else:
            print('error1')
    
    elif n == 2:
        if year_i == 2017:
            cond1 = (df_.cerrado_19 == 1) & (df_.abierto_18 == 1)
            cond2 = (df_.cerrado_18 == 1) & (df_.abierto_17 == 1)
            cond3 = (df_.cerrado_19 == 1) & (df_.cerrado_18 != 1) & (df_.abierto_17 == 1)
        
            df_['target'] = np.where(cond1 | cond2 | cond3, 1 ,0)  
    
        elif year_i == 2016:
            cond1 = (df_.cerrado_19 == 1) & (df_.abierto_18 == 1)
            cond2 = (df_.cerrado_18 == 1) & (df_.abierto_17 == 1)
            cond3 = (df_.cerrado_17 == 1) & (df_.abierto_16 == 1)
            cond4 = (df_.cerrado_19 == 1) & (df_.cerrado_18 != 1) & (df_.abierto_17 == 1)
            cond5 = (df_.cerrado_18 == 1) & (df_.cerrado_17 != 1) & (df_.abierto_16 == 1)
        
            df_['target'] = np.where(cond1 | cond2 | cond3 | cond4 | cond5, 1 ,0)
        else:
            print('error2')
        
    else: 
        print('error3')
            
    return df_


# function to calculate the target variable: locals closed the lat n years, stating the analysis in year m
def target2(df_,n):
    if n == 1:
        df_['target'] = np.where(df_.cerrado_19 == 1, 1,0)
        
    elif n == 2:
        df_['target'] = np.where((df_.cerrado_19 == 1) | (df_.cerrado_18 == 1), 1,0)
        
    elif n == 3:
        cond3 = ((df_.cerrado_19 == 1) | (df_.cerrado_18 == 1) | (df_.cerrado_17 == 1))
        df_['target'] = np.where(cond3, 1,0)
        
    elif n == 4:
        cond4 = ((df_.cerrado_19 == 1) | (df_.cerrado_18 == 1) 
                 | (df_.cerrado_17 == 1) | (df_.cerrado_16 == 1))
        df_['target'] = np.where(cond4, 1,0)
        
    else:
        print('error')
    
    return df_


# Genero columnas con los abiertos y cerrados en cada año:   
#- abiertos cada año (ej: abiertos no existentes el año anterior)   
#- cerrados cada año (ej 2019: cerrados y uso vivienda no cerrados/uso vivienda en años anteriores)

def sit_year(df):
    df_ = df.copy()
    cond1 = ((df_.desc_sit_loc_modif_19 == 'Cerrado') |
                                 (df_.desc_sit_loc_modif_19 == 'Uso vivienda'))  
                                 
    cond2 = ((df_.desc_sit_loc_modif_18 != 'Cerrado') |
                                 df.desc_sit_loc_modif_18.isnull())
    cond3 = ((df_.desc_sit_loc_modif_19.notnull()) &
                                 (df_.desc_sit_loc_modif_18.isnull()))
    df_['cerrado_19'] = np.where(cond1 & cond2, 1 ,0)
    df_['abierto_19'] = np.where(cond3, 1 ,0)
        
    cond4 = ((df_.desc_sit_loc_modif_18 == 'Cerrado') |
                                 (df_.desc_sit_loc_modif_18 == 'Uso vivienda'))  
                                 
    cond5 = ((df_.desc_sit_loc_modif_17 != 'Cerrado') |
                                 df.desc_sit_loc_modif_17.isnull())
    cond6 = ((df_.desc_sit_loc_modif_18.notnull()) &
                                 (df_.desc_sit_loc_modif_17.isnull()))
    df_['cerrado_18'] = np.where(cond4 & cond5, 1 ,0)
    df_['abierto_18'] = np.where(cond6, 1 ,0)
        
    cond7 = ((df_.desc_sit_loc_modif_17 == 'Cerrado') |
                                 (df_.desc_sit_loc_modif_17 == 'Uso vivienda'))
    cond8 = ((df_.desc_sit_loc_modif_16 != 'Cerrado') |
                                 df.desc_sit_loc_modif_16.isnull())
    cond9 = ((df_.desc_sit_loc_modif_17.notnull()) &
                                 (df_.desc_sit_loc_modif_16.isnull()))
    df_['cerrado_17'] = np.where(cond7 & cond8, 1 ,0)
    df_['abierto_17'] = np.where(cond9, 1 ,0)
       
    cond10 = ((df_.desc_sit_loc_modif_16 == 'Cerrado') |
                                 (df_.desc_sit_loc_modif_16 == 'Uso vivienda'))  
                                 
    cond11 = ((df_.desc_sit_loc_modif_15 != 'Cerrado') |
                                 df.desc_sit_loc_modif_15.isnull())
    cond12 = ((df_.desc_sit_loc_modif_16.notnull()) &
                                 (df_.desc_sit_loc_modif_15.isnull()))
    df_['cerrado_16'] = np.where(cond10 & cond11, 1 ,0)
    df_['abierto_16'] = np.where(cond12, 1 ,0)
    
    return df_

# función que estima los id_epigrafes con un número de id_epigrafe > m y donde el % # id_epigrafe target/locales con este id es superior a n

def act_filter_id(df,n,m):
    df__ = df.copy()
    df_zero = df__[((df__.desc_sit_loc_modif_19 != 'Cerrado') | (df__.desc_sit_loc_modif_19 != 'Uso vivienda')) & 
                  (df__.target == 0)]
    df_ones = df__[df__.target == 1]
    tablon = [df_zero,df_ones]
    df_ = pd.concat(tablon)
    act_count = df_['id_epigrafe'].value_counts()
    ones = df_ones['id_epigrafe'].value_counts()
    df_ = pd.concat([act_count, ones], axis=1,sort = False)
    df_ = df_.rename(columns = {'id_epigrafe':'ones'})
    names = df_.columns.tolist()
    names[0] = 'act_count'
    df_.columns = names
    df_.ones.fillna(0, inplace=True)
    df_['perc'] = df_.apply(lambda x: x['ones']/x['act_count'],axis=1)
    df_.sort_values(by='perc', ascending=False,inplace=True)
    df_f = df_[(df_.act_count > n) & (df_.perc > m) ]
    return df_f.index.values.astype(int)

# función que devuelve un df los desc_epigrafes con un número de id_epigrafe > m y donde el % # id_epigrafe target/locales con este id es superior a n

def act_filter_desc(df,n,m):
    df__ = df.copy()
    df_zero = df__[((df__.desc_sit_loc_modif_19 != 'Cerrado') | (df__.desc_sit_loc_modif_19 != 'Uso vivienda')) & 
                  (df__.target == 0)]
    df_ones = df__[df__.target == 1]
    tablon = [df_zero,df_ones]
    df_ = pd.concat(tablon)
    act_count = df_['desc_epigrafe'].value_counts()
    ones = df_ones['desc_epigrafe'].value_counts()
    df_ = pd.concat([act_count, ones], axis=1,sort = False)
    df_ = df_.rename(columns = {'desc_epigrafe':'ones'})
    names = df_.columns.tolist()
    names[0] = 'act_count'
    df_.columns = names
    df_.ones.fillna(0, inplace=True)
    df_['perc'] = df_.apply(lambda x: x['ones']/x['act_count'],axis=1)
    df_.sort_values(by='perc', ascending=False,inplace=True)
    df_f = df_[(df_.act_count > n) & (df_.perc > m) ]
    return df_f

# function to calculate 'id_act_norm' > (m == % # id_act_norm target/locales) and the # of total locals with this 'id_act_norm' > n

def act_filter_id_norm(df,n,m):
    df__ = df.copy()
    df_zero = df__[((df__.desc_sit_loc_modif_19 != 'Cerrado') | (df__.desc_sit_loc_modif_19 != 'Uso vivienda')) & 
                  (df__.target == 0)]
    df_ones = df__[df__.target == 1]
    tablon = [df_zero,df_ones]
    df_ = pd.concat(tablon)
    act_count = df_['id_act_norm'].value_counts()
    ones = df_ones['id_act_norm'].value_counts()
    df_ = pd.concat([act_count, ones], axis=1,sort = False)
    df_ = df_.rename(columns = {'id_act_norm':'ones'})
    names = df_.columns.tolist()
    names[0] = 'act_count'
    df_.columns = names
    df_.ones.fillna(0, inplace=True)
    df_['perc'] = df_.apply(lambda x: x['ones']/x['act_count'],axis=1)
    df_.sort_values(by='perc', ascending=False,inplace=True)
    df_f = df_[(df_.act_count > n) & (df_.perc > m) ]
    return df_f.index.values.astype(int)

# function to calculate 'desc_act_norm' > (m == % # desc_act_norm target/locales) and the # of total locals with this 'desc_act_norm' > n

def act_filter_desc_norm(df,n,m):
    df__ = df.copy()
    df_zero = df__[((df__.desc_sit_loc_modif_19 != 'Cerrado') | (df__.desc_sit_loc_modif_19 != 'Uso vivienda')) & 
                  (df__.target == 0)]
    df_ones = df__[df__.target == 1]
    tablon = [df_zero,df_ones]
    df_ = pd.concat(tablon)
    act_count = df_['desc_act_norm'].value_counts()
    ones = df_ones['desc_act_norm'].value_counts()
    df_ = pd.concat([act_count, ones], axis=1,sort = False)
    df_ = df_.rename(columns = {'desc_act_norm':'ones'})
    names = df_.columns.tolist()
    names[0] = 'act_count'
    df_.columns = names
    df_.ones.fillna(0, inplace=True)
    df_['perc'] = df_.apply(lambda x: x['ones']/x['act_count'],axis=1)
    df_.sort_values(by='perc', ascending=False,inplace=True)
    df_f = df_[(df_.act_count > n) & (df_.perc > m) ]
    return df_f



# Function that generates an intermediate status to unify the locals with the same id_local and more than one activity, in a # # single epigrafe (the first found)
def new_col2(df):
    act = []
    for i in range(len(df)):
        for j in range(len(df.columns.values)-2):
            if df.iloc[i][df.columns.values[j+1]] > 0:
                text = df.columns.values[j+1]
        act.append(text)
    return act

# Funcion que calcula el número de locales de la misma actividad dentro de una distancia = dist
def num_loc_dist(df,dist):
    pointn = (0,0)
    num_loc_d = []
    for i in range(len(df)):
        point1 = (df.lat[i],df.lon[i])
        distance = []
        for j in range(len(df)):
            if df.desc_epigrafe[i] == df.desc_epigrafe[j]:
                pointn = (df.lat[j],df.lon[j])
                distance.append(geodesic(point1, pointn).meters)#          
        num_loc_d.append(len(list(filter(lambda num: num < dist,distance)))-1)
        
    return num_loc_d

# Function to standardize the activity. Those activities with less than median(#locals/activity)==act in Madrid, are assigned the desc_act_norm == 'OTRAS ACTIVIDADES'.
def norm_act(df,act):
    if df in act:
        return 'OTRAS ACTIVIDADES'            
    else:
        return df
# Function to standardize the activity. Those activities with less than median(#locals/activity)==act in Madrid, are assigned the id_act_norm == 999999.
def norm_id_act(df_act,df_id,act):
    if df_act in act:
        return int(999999)            
    else:
        return df_id
