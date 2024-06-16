import os 
import pandas as pd
import re

os.chdir("C:\\Users\\halol\\Desktop\\Estudio\\Tesis\\datasets\\finals")

df = pd.read_excel('to_work_2.xlsx')


def price_clear(valor):
    print(valor)
    new_valor = str(valor).replace('-','')
    new_valor = float(new_valor)
    return new_valor

def km_clear(valor):
    if valor == '-' or valor == 'nan':
        return None
    new_valor = str(valor).replace("km",'').replace('.','')
    new_valor = int(new_valor)
    return new_valor

def potenza_clear(text, pattern):
    match = pattern.search(text)
    if match:
        return float(match.group(1))
    else:
        return None
    
def cilindrata_clear(valor):
    if valor == '-' or valor == 'nan':
        return None
    new_valor = str(valor).replace("cm³",'').replace('.','')
    new_valor = float(new_valor)
    return new_valor

def peso_vuoto_clear(valor):
     if valor == '-' or valor == 'nan':
         return None
     new_valor = str(valor).replace("kg",'').replace('.','')
     new_valor = float(new_valor)
     return new_valor

def extract_consumption(text, pattern):
    match = pattern.search(str(text))
    if match:
        consumption_value = match.group(1).replace(',', '.').rstrip('.') 
        return float(consumption_value)
    else:
        return None
    
def emission_clear(valor):
    print(valor)
    if valor == '-' or str(valor) == 'nan':
        return None
    new_valor = str(valor).replace(' g/km (comb.)','').replace(',','.')
    new_valor = float(new_valor)
    return new_valor

def anno_clear(valor):
    valor = str(valor)
    new_valor = valor.split('-')[0]
    return new_valor

def carburante_clear(valor):
    new_valor = valor.replace(',','')
    return new_valor

def replace_dash(value):
    return None if value == '-' else value

def spliter_slash(valor):
    if valor is None:
        return None
    new_valor = [part.strip() for part in valor.split('/')]
    return new_valor

def spliter_point(valor):
    if valor is None or isinstance(valor, float) or valor == float('nan'):
        return None
    print(valor)
    new_valor = [part.strip() for part in valor.split(',')]
    return new_valor

    
pattern_kw = r'(\d+)\s*kW'
pattern_cv = r'(\d+)\s*CV'
pattern_comb = r'([\d,]+)\s*l/100 km \(comb.\)'
pattern_urbano = r'([\d,]+)\s*l/100 km \(urbano\)'
pattern_extraurbano = r'([\d,]+)\s*l/100 km \(extraurbano\)'


df.columns


df['Prezzo'] = df['Prezzo'].apply(price_clear)
df['Chilometraggio'] = df['Chilometraggio'].apply(km_clear)
df['Potenza_kW'] = df['Potenza'].apply(lambda x: potenza_clear(x, re.compile(pattern_kw)))
df['Potenza_CV'] = df['Potenza'].apply(lambda x: potenza_clear(x, re.compile(pattern_cv)))
df['Cilindrata'] = df['Cilindrata'].apply(cilindrata_clear)
df['Peso a vuoto'] = df['Peso a vuoto'].apply(peso_vuoto_clear)
df['Consumo_comb'] = df['Consumo di carburante2,8'].apply(lambda x: extract_consumption(x, re.compile(pattern_comb)))
df['Consumo_urbano'] = df['Consumo di carburante2,8'].apply(lambda x: extract_consumption(x, re.compile(pattern_urbano)))
df['Consumo_extraurbano'] = df['Consumo di carburante2,8'].apply(lambda x: extract_consumption(x, re.compile(pattern_extraurbano)))
df['Emissioni CO₂2,8'] = df['Emissioni CO₂2,8'].apply(emission_clear)
df['Anno'] = df['Anno'].apply(anno_clear)
df['Carburante'] = df['Carburante'].apply(carburante_clear)
df = df.applymap(replace_dash)
df['Carburante'] = df['Carburante'].apply(spliter_slash)
df['Comfort'] = df['Comfort'].apply(spliter_point)
df['Intrattenimento / Media'] = df['Intrattenimento / Media'].apply(spliter_point)
df['Sicurezza'] = df['Sicurezza'].apply(spliter_point)
df['Extra'] = df['Extra'].apply(spliter_point)

df.to_excel('no_dummy_dataset.xlsx',index=False)

dummy_cols = ['Marca','Carrozzeria','Tipo di cambio','Venditore','Classe emissioni','Colore','Trazione']

def dummyfier(df,dummy_cols):
    d_df = df.copy()
    for col in dummy_cols:
        print(col)
        dummy_df = pd.get_dummies(d_df[col], prefix='dummy_' + col, prefix_sep='_')
        d_df = pd.concat([d_df, dummy_df], axis=1)
    return d_df

d_df = dummyfier(df,dummy_cols)

d_df.columns

dummy_cols_list = set([el.strip() for lst in d_df['Carburante'] if lst is not None for el in lst])

for col in dummy_cols_list:
    d_df[f'dummy_Carburante_{col}'] = d_df['Carburante'].apply(lambda x: 1 if x is not None and col in x else 0)

d_df.to_excel('dummy_dataset_2.xlsx',index=False)

# dummy_cols_list = []
# for lst in d_df['Carburante']:
#     if lst is not None:
#         for el in lst:
#             if el in dummy_cols_list:
#                 continue
#             else:
#                 dummy_cols_list.append(el.strip())
# dummy_cols_list = list(set(dummy_cols_list))        


# for d in dummy_cols_list:
#     d_df[f'dummy_Carburante_{d}'] = []
#     for element in d_df['Carburante']:
#         if element is not None:
#             if d in element:
#                 d_df[f'dummy_Carburante_{d}'].append(1)
#             else:
#                 d_df[f'dummy_Carburante_{d}'].append(0)    
#         else:
#             d_df[f'dummy_Carburante_{d}'].append(None)
            
        


string_columns = d_df.select_dtypes(include='object').columns

for columna in d_df.columns:
    if 'dummy' in columna:
        d_df[columna] = d_df[columna].astype(bool)
int_columns = ['Posti','Porte','Marce','Cilindri','Prezzo']

float_columns = d_df.select_dtypes(include='float64').columns
bool_columns = d_df.select_dtypes(include='bool').columns


df_cleaned = d_df.dropna(subset=['Adress'])
df_filtrado = df_cleaned[df_cleaned['Adress'].str.endswith(', IT')]
string_columns = string_columns.drop('Modello')

r_df = df_filtrado.drop(columns=string_columns)
r_df = r_df.drop(columns=['Proprietari'])
r_df[bool_columns] = r_df[bool_columns].astype(int)

na_df = {'Columna':[], 'NaNs':[]}

for column in r_df.columns:
    na_count = r_df[column].isna().sum()
    na_df['Columna'].append(column)
    na_df['NaNs'].append(na_count)
    
na_df = pd.DataFrame(na_df)    

def none_filler(r_df,int_columns):
    ## Esta funcion lo que hace es rellenar los Nan con valores especificos, 
    ## para el caso de las columnas 'Posti','Porte','Marce','Cilindri','Prezzo'
    ## las considerara como datos int por lo que sostituira los Nan por la moda de todos los datos
    ## mientras que para el resto de las columnas que no sean booleanas pues tomara la media
    
    
    all_models = list(set(r_df['Modello']))
    for modelo in all_models:
        modelo_data = r_df[r_df['Modello'] == modelo]
        if modelo_data.isna().all(axis=0).any():
            print("Al menos una columna tiene todos los valores NaN")
            continue
        else:
            for column in modelo_data.columns:
                if 'dummy' in column or 'Modello' in column or 'Anno' in column:
                    continue
                elif column in int_columns:
                    
                    moda = modelo_data[column].mode()[0]
                    modelo_data[column] = modelo_data[column].fillna(moda)
                else:
                    
                    media = modelo_data[column].mean()
                    modelo_data[column] = modelo_data[column].fillna(media)
        r_df[r_df['Modello'] == modelo] = modelo_data            
    new_r_df = r_df
    return new_r_df

def eliminar_columnas_constantes(df):
    columnas_constantes = [columna for columna in df.columns if df[columna].nunique() == 1]
    nuevo_df = df.drop(columnas_constantes, axis=1)
    return nuevo_df


nona_full = none_filler(df_filtrado,int_columns)

nona_full2 = nona_full.dropna()
nona_full2 = nona_full2.drop(columns = ['Modello'])
    
no_na_df = r_df.dropna()

no_na_df[bool_columns] = no_na_df[bool_columns].astype(int)

nona_full2 = eliminar_columnas_constantes(nona_full2)

nuevos_nombres = {columna: columna.replace(' ','_') for columna in nona_full2.columns}
nona_full2.rename(columns=nuevos_nombres, inplace=True)

no_na_df.to_excel('final_noNA_dataset_towork.xlsx',index=False)
r_df.to_excel('final_dataset_towork.xlsx',index=False)
nona_full2.to_excel('final_full_Nona_dataset_towork.xlsx',index=False)

for element in list(r_df.columns):
    print(element)
        
for col in list(d_df.columns):
    if 'Carburante' in col:
        print(col)