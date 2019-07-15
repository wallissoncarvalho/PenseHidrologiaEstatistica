import pandas as pd
import calendar
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.figure_factory as ff
init_notebook_mode(connected=True)
def gantt_plot(dados): 
    """Plota o gráfico de gantt dos dados, mostrando a sua disponibilidade temporal;
       Para funcionamento do código, deve-se passar um dataframe onde cada coluna refere-se aos dados de uma estação;
       O index deve ser um datetime.
    """
    df=[]
    postos=list(dados.columns.values)
    for j in range(len(postos)):
        if dados[postos[j]].isnull().values.any()==True:
            serie_completa=dados[postos[j]]
            falhas_serie_completa=serie_completa.isnull().groupby(pd.Grouper(freq='1MS')).sum().to_frame()
            periodos_sem_falha=falhas_serie_completa.loc[falhas_serie_completa[postos[j]] < 7].diff(1) #UM MÊS COM AUSÊNCIA DE 7 DADOS É CONSIDERADO COM FALHA
            diff=[]
            for i in range(len(periodos_sem_falha)):
                if i==0:
                    diff.append(0)
                else:
                    if periodos_sem_falha.index.year[i]-periodos_sem_falha.index.year[i-1]==0:
                        if periodos_sem_falha.index.month[i]-periodos_sem_falha.index.month[i-1]!=1:
                            diff.append(99)
                        else:
                            diff.append(0)
                    elif periodos_sem_falha.index.year[i]-periodos_sem_falha.index.year[i-1]==1:
                        if periodos_sem_falha.index.month[i]-periodos_sem_falha.index.month[i-1]!=-11:
                            diff.append(99)
                        else:
                            diff.append(0)
                    else:
                        diff.append(99)
            periodos_sem_falha=pd.DataFrame(diff,periodos_sem_falha.index,columns={postos[j]})
            if periodos_sem_falha.shape[0]>1:
                Task1=postos[j]
                Resource1='Periodo com Dados'
                data=periodos_sem_falha.index[0]
                periodos_sem_falha=periodos_sem_falha[1:]
                Start1=str(data.year)+'-'+str(data.month)+'-'+'01'
                Finish1=0
                i=0
                while i < (len(periodos_sem_falha)-1):
                    if periodos_sem_falha[postos[j]][i]==0:
                        i+=1
                    else:
                        data=periodos_sem_falha.index[i-1]
                        n,ultimo_dia=calendar.monthrange(data.year,data.month)
                        Finish1=str(data.year)+'-'+str(data.month)+'-'+str(ultimo_dia)
                        dici=dict(Task=Task1,Start=Start1,Finish=Finish1,Resource=Resource1)
                        df.append(dici)
                        data=periodos_sem_falha.index[i]
                        Start1=str(data.year)+'-'+str(data.month)+'-'+'01'
                        Finish1=0
                        i+=1       
                if Finish1==0:
                    data=periodos_sem_falha.index[i]
                    n,ultimo_dia=calendar.monthrange(data.year,data.month)
                    Finish1=str(data.year)+'-'+str(data.month)+'-'+str(ultimo_dia)
                    dici=dict(Task=Task1,Start=Start1,Finish=Finish1,Resource=Resource1)
                    df.append(dici)
            else:
                print('Posto {} não possui meses com dados significativos'.format(postos[j]))
        else:
            Task1=postos[j]
            Resource1='Periodo com Dados'
            data=dados[postos[j]].index[0]
            periodos_sem_falha=periodos_sem_falha[1:]
            Start1=str(data.year)+'-'+str(data.month)+'-'+'01'
            data=dados[postos[j]].index[-1]
            Finish1=str(data.year)+'-'+str(data.month)+'-'+'01'
            dici=dict(Task=Task1,Start=Start1,Finish=Finish1,Resource=Resource1)
            df.append(dici)
    colors={'Periodo com Dados': 'rgb(0,191,255)'}
    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,showgrid_x=True, showgrid_y=True, height=400,width=800, group_tasks=True)
    iplot(fig)

