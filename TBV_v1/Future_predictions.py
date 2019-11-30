#!/usr/bin/env python
# coding: utf-8

import pandas as pd


'''Funcion that return the list of commercial premises to close in 3 years
Input:
- Dataframe with the commercial premises to perform prediction
- Dataframe with all the commercial premises
- Classifier

Returns:
- Dataframe with the commercial premises to close with all the variables in Dataframe with all commercial premises
- Dataframe with the commercial premises to close with variables of interest (name, district, category)
- Dataframe with the prediction and probabilidades
'''

def future_preds(df_open, df_total, clf):
    X_open = df_open
    df_locals = df_total.reset_index()
    
    # drop target variable, predict and predict proba of the target
    X_open_t = X_open.drop('target',axis=1)
    pred_open = clf.predict(X_open_t)
    pred_open_prob = clf.predict_proba(X_open_t)

    # Join prediction with local odentifier 
    data_r = pd.DataFrame()
    data_r['pred'] = pd.Series(pred_open)
    data_r['pred_proba'] = pd.Series(pred_open_prob[:,1])
    df1 = X_open_t.reset_index()
    df2 = df1['id_local']
    df3 = pd.concat([df2,data_r],axis=1)

    # Identify Class 1
    df3_ones = df3[df3.pred==1]

    # Commercial premises info and filter Class 0
    locals_to_close = df_locals[df_locals.id_local.isin(df3_ones.id_local.values)].copy()

    # Select info and show
    locals_to_close_clean = locals_to_close[['id_local','desc_distrito_local','desc_tipo_agrup','rotulo','desc_epigrafe']]
    return (locals_to_close_clean,locals_to_close,df3)

