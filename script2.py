import pandas as pd
import numpy as np
import re
import os
from pathlib import Path
import gc
from zipfile import ZipFile
from unidecode import unidecode
import posixpath as pp

project_dir = Path("notebook.ipynb").resolve().parents[0]
print(project_dir)

df = pd.read_stata('data_edited.dta')
df.columns = [ x.replace('_','',2).lower() for x in df.columns]
df = df.drop('index',axis=1)
df['ano'] = df['ano'].astype('int')
tarifas = pd.read_csv(f'tarifas-homologadas-distribuidoras-energia-eletrica.csv',parse_dates=['DatGeracaoConjuntoDados','DatInicioVigencia',
 'DatFimVigencia'])
relacao = pd.read_csv(f'relacao-cidade-distribuidora-rs-2017.csv')
relacao = relacao.rename({'Concessionária / Permissionária':'distribuidora'}, axis=1)
tarifas_join = pd.merge(left=relacao, right=tarifas, left_on='distribuidora', right_on='SigAgente')
tarifas_join['tarifa_ano_inicio'] = tarifas_join['DatInicioVigencia'].dt.year
tarifas_join['tarifa_ano_fim'] = tarifas_join['DatFimVigencia'].dt.year
tarifas_join = tarifas_join.drop(['Estado','DatGeracaoConjuntoDados','DscDetalhe','SigAgenteAcessante','NomPostoTarifario','DscSubGrupo'], axis=1)
tarifas_join = tarifas_join.rename({'Município':'municpio'},axis=1)
merge = pd.merge(left=df,right=tarifas_join, left_on=['municpio','ano'], right_on=['municpio','tarifa_ano_inicio'], how='inner')
merge.to_csv(f'data_edited.csv', index=False)