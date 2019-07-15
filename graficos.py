import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from math import ceil, log
import matplotlib.ticker as ticker

def curva_permanencia(dados,logscale=True):
    plt.figure(num=None, figsize=(15, 12), dpi=100, facecolor='w', edgecolor='k')
    ymax=0
    #ax = plt.gca()
    for name in dados.columns:
        serie=dados[name].dropna()
        n=len(serie)
        y = np.sort(serie)
        y = y[::-1]
        if ymax < y.max():
            ymax=y.max()
        x = (np.arange(1,n+1) / n)*100
        _ = plt.plot(x,y,linestyle='-') 
    plt.legend(list(dados.columns), loc='best')
    plt.margins(0.02) 
    if logscale==True:
        ticks = 10**np.arange(1,ceil(log(ymax,10)) + 1,1)
        ticks[-1:]+=1
        plt.yticks(list(ticks))
        plt.yscale('log')
        plt.tick_params(axis='y', which='minor')
        
    _ = plt.xlabel('Probabilidade de excedência ou igualdade (%)')
    _ =  plt.ylabel('Vazão m³/s')
    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    plt.xticks(np.arange(0,101,step=10))
    plt.grid(b=True,which='both')
    plt.show()
    

        
        
def boxplot_mes(dados,nrows,ncolumns,figsize):
    falhas_mensais=dados.isnull().groupby(pd.Grouper(freq='M')).sum()
    acumulado_mensal=dados.groupby(pd.Grouper(freq='M')).sum()
    fig1, axs = plt.subplots(nrows, ncolumns, figsize=figsize, constrained_layout=True, sharey='all')
    def trim_axs(axs, N):
        """little helper to massage the axs list to have correct length..."""
        axs = axs.flat
        for ax in axs[N:]:
            ax.remove()
        return axs[:N]
    axs = trim_axs(axs, ncolumns)
    for ax, coluna in zip(axs,dados.columns):
        #REMOVER MESES COM 15% DE FALHA
        falha_coluna=falhas_mensais[coluna].to_frame()
        acumulado_coluna=acumulado_mensal[coluna].to_frame()
        falha_periodo=falha_coluna.loc[falha_coluna[coluna] > 4]
        acumulado_coluna=acumulado_coluna.drop(index=falha_periodo.index).sort_index()
        serie_por_mes=acumulado_coluna.groupby(by=acumulado_coluna.index.month)
        meses=[]
        for group in serie_por_mes.groups:
            meses.append(list(serie_por_mes.get_group(group)[coluna]))
        ax.boxplot(meses)
        ax.set_title('Estação '+coluna)
        ax.set_xlabel("Mês do Ano")
        ax.set_ylabel("Acumulado Mensal (mm/mês)")
    

def prec_mensal(dados,nrows,ncolumns,figsize):
    falhas_mensais=dados.isnull().groupby(pd.Grouper(freq='M')).sum()
    acumulado_mensal=dados.groupby(pd.Grouper(freq='M')).sum()
    fig1, axs = plt.subplots(nrows, ncolumns, figsize=figsize, constrained_layout=True, sharey='all')
    def trim_axs(axs, N):
        """little helper to massage the axs list to have correct length..."""
        axs = axs.flat
        for ax in axs[N:]:
            ax.remove()
        return axs[:N]
    axs = trim_axs(axs, ncolumns)
    for ax, coluna in zip(axs,dados.columns):
        #REMOVER MESES COM 15% DE FALHA
        falha_coluna=falhas_mensais[coluna].to_frame()
        acumulado_coluna=acumulado_mensal[coluna].to_frame()
        falha_periodo=falha_coluna.loc[falha_coluna[coluna] > 4]
        acumulado_coluna=acumulado_coluna.drop(index=falha_periodo.index).sort_index()
        serie_por_mes=acumulado_coluna.groupby(by=acumulado_coluna.index.month).mean()
        media=serie_por_mes[coluna].mean()
        xmin=list(serie_por_mes.index)[0]
        xmax=list(serie_por_mes.index)[-1]
        ax.bar(serie_por_mes.index,serie_por_mes[coluna],align='center')
        ax.hlines(y=media,xmin=xmin,xmax=xmax,linewidth=2,color='r',linestyle='dashed')
        ax.legend(('Média','Média Mensal'), loc='upper right')
        ax.set_title('Estação '+coluna)
        ax.set_xlabel('Mês do ano',fontsize=12)
        ax.set_xticks(np.arange(1,12.1,step=1))
        ax.set_yticks(np.arange(0,400,step=50))
        ax.set_ylabel('Precipitação (mm/mês)',fontsize=12)

def prec_media_mensal(dados_chuva,dados_vazao):
    media_chuva = pd.DataFrame()
    falhas_mensais=dados_chuva.isnull().groupby(pd.Grouper(freq='M')).sum()
    acumulado_mensal=dados_chuva.groupby(pd.Grouper(freq='M')).sum()
    for coluna in dados_chuva.columns:
        falha_coluna=falhas_mensais[coluna].to_frame()
        acumulado_coluna=acumulado_mensal[coluna].to_frame()
        falha_periodo=falha_coluna.loc[falha_coluna[coluna] > 4]
        acumulado_coluna=acumulado_coluna.drop(index=falha_periodo.index).sort_index()
        serie_por_mes=acumulado_coluna.groupby(by=acumulado_coluna.index.month).mean()
        media_chuva=pd.concat([media_chuva,serie_por_mes],axis=1)
    media_artmetica=media_chuva.mean(axis=1)
    
    media_vazao = pd.DataFrame()
    falhas_mensais=dados_vazao.isnull().groupby(pd.Grouper(freq='M')).sum()
    media_mensal=dados_vazao.groupby(pd.Grouper(freq='M')).mean()
    for coluna in dados_vazao.columns:
        falha_coluna=falhas_mensais[coluna].to_frame()
        media_coluna=media_mensal[coluna].to_frame()
        falha_periodo=falha_coluna.loc[falha_coluna[coluna] > 4]
        media_coluna=media_coluna.drop(index=falha_periodo.index).sort_index()
        serie_por_mes=media_coluna.groupby(by=media_coluna.index.month).mean()
        media_vazao=pd.concat([media_vazao,serie_por_mes],axis=1)
        
    fig, ax1 = plt.subplots(figsize=(9,9))

    color = 'tab:red'
    ax1.set_xlabel('Mês do ano', fontsize=14)
    ax1.set_ylabel('Precipitação (mm/mês)',fontsize=14)
    ax1.bar(media_artmetica.index,media_artmetica,align='center')
    #ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


    ax2.set_ylabel('Vazão (m³/s)',fontsize=14)  # we already handled the x-label with ax1
    ax2.plot(media_vazao.index,media_vazao[media_vazao.columns[0]],linestyle='-',color='red')


    plt.show()
