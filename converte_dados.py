import os
import pandas as pd
import calendar
    
def hidroweb(dir_dados): 
    """Converte os dados do hidroweb para um dataframe onde cada coluna referese à uma estação;
       dir_dados -> Diretório no computador onde estão os dados das estações no formato .csv;
       PARA MELHOR SEPARAR O DATAFRAME DEIXAR OS ARQUIVOS DE APENAS UMA VARIÁVEL EM dir_dados
    """     
    dados=pd.DataFrame()
    for root,dirs,files in os.walk(dir_dados):
        for file in files:
            if file[-3:] == 'csv':
                if file[:6]=='vazoes':
                    skiprows,coluna_inicio,coluna_fim=14,16,15
                elif file[:6]=='chuvas':
                    skiprows,coluna_inicio,coluna_fim=13,13,12
                elif file[:5]=='cotas':
                    skiprows,coluna_inicio,coluna_fim=14,16,15
                df=pd.read_csv(dir_dados+'\\'+file,sep=';',skiprows=skiprows,header=None)
                #df[2]=df[2].apply(lambda x:str(x))
                df[2]=df[2].apply(lambda x:'01'+x[2:])
                df[2] =  pd.to_datetime(df[2], format='%d/%m/%Y')
                df=df.loc[df.groupby(2)[1].idxmax()] #REMOVE OS DADOS DUPLICADOS QUE COM CONSISTÊNCIA 1
                df.index=df[2]
                #TRANSFORMA OS DADOS PARA SÉRIE CONTÍNUA COM UMA COLUNA:
                lista_series_mensais=[]
                for data in list(df[2]):
                    ultimo_dia=calendar.monthrange(data.year,data.month)[1]
                    mes=pd.date_range(data,periods=ultimo_dia, freq='D')
                    serie_linha=pd.Series(df.loc[data,coluna_inicio:coluna_fim+ultimo_dia], name='Dados')
                    serie = pd.Series(list(serie_linha),index = mes)
                    lista_series_mensais.append(serie)
                serie_completa=pd.concat(lista_series_mensais)
                serie_completa=serie_completa.apply(lambda x: float(x.replace(',','.')) if isinstance(x,str) else x)
                serie_completa=serie_completa.sort_index()
                data_index = pd.date_range(serie_completa.index[0], serie_completa.index[-1], freq='D')
                serie_completa=serie_completa.reindex(data_index)
                serie_completa.sort_index()
                serie_completa=serie_completa.to_frame()
                serie_completa=serie_completa.rename(columns={0:file[-12:-4]})
                dados=pd.concat([dados,serie_completa],axis=1)        
    dados.dropna(axis=1,how='all',inplace=True)
    data_index = pd.date_range(dados.index[0], dados.index[-1], freq='D')
    dados=dados.reindex(data_index)  
    return dados

def ons(dir_dados,id_station=all):
    dados = pd.read_excel(dir_dados,skiprows=5)
    dados = dados[1:]
    dados[dados.columns[0]]=dados[dados.columns[0]].apply(lambda x:'0'+ x if len(x)==10 else x)
    mes = {'jan':'01','fev':'02','mar':'03','abr':'04','mai':'05','jun':'06','jul':'07','ago':'08','set':'09','out':'10','nov':'11','dez':'12'}
    dados[dados.columns[0]]=dados[dados.columns[0]].apply(lambda x:x[:3]+mes[x[3:6]]+x[6:])
    dados[dados.columns[0]]=pd.to_datetime(dados[dados.columns[0]], format='%d/%m/%Y')
    dados.index=dados[dados.columns[0]]
    dados=dados.drop(dados.columns[0],axis=1)
    if id_station != all:
        for column in dados.columns:
            if id_station == column[-(len(id_station)+1):-1]:
                coluna = column
    return dados[coluna].to_frame()