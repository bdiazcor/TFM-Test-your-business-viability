### Kshool-TFM-
DS Master TFM repository. Structure:

#### 1) Data:   
Contains data files and data description:
>
- **censolocales**:  
>>
Base data for project. Contains Madrid open data (https://datos.madrid.es/) with info about stores,        activities, licences, status, neighborhood id, local coordinates, etc split in three files /month/year       (since 2015 and quarterly in 2014):  
>>
- OPEN DATA Localesyyyymm.csv: stores info  
- OPEN DATA Locales-Epigrafesyyyymm.csv: stores info + activities  
- OPEN DATA Licenciasyyyymm: stores info + licences status  
>>
More info about fields meaning: Estructura_DS_FicheroCLA.pdf; Estructura_DS_FicheroCLA_Licencias.pdf;       EpigrafesActividadEconomica.pdf   
        
- **PF**: Madrid floating population. Based on one standard week. PF_README for details.    

- **Other**:  
>>- CALLEJERO_VIGENTE_BARRIOS_201809.csv: Madrid neighborhoods per district. Includes ids
>>- CALLEJERO_VIGENTE_DISTRITOS_201809.csv: Madrid districts with ids.
>>- PANEL_INDICADORES_2018.pdf: 2018 Madrid neighborhoods main population KPIs study.

#### 2) TBV_V1: 
TFM v1 (MPV) notebooks and code. Structure:   
>
- **Data_preparation.ipynb**: contains the table with stores info since 2016. For clarity when reading the Notebook:  
>>- df_loc: info stores
>>- df_epi: info activities
>>- df_licences: info licences




