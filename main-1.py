#------------------------------------------Trabalho Prático I de Estatística e Probabilidade----------------------------------------------------# 
#----------------------------------------Engenharia de Computação - Campus Coração Eucarístico--------------------------------------------------# 
#-------------------------------------------------- PMG - Noite - G1/T1 - 2024/2----------------------------------------------------------------#
#---------------------------------------------------------Turma 82.27.101-----------------------------------------------------------------------#
#------------------------------------------------Alunos: Bruno Henrique Reis Almeida------------------------------------------------------------#
#----------------------------------------------------Cleber Marcos Pereira dos Reis-------------------------------------------------------------#
#------------------------------------------------------Gabriel da Silva Cassino-----------------------------------------------------------------#
#-----------------------------------------------Luiz Henrique Miranda Pacheco de Castro---------------------------------------------------------# 
#-----------------------------------------------------------Orientações: -----------------------------------------------------------------------#

#Criado: 31-08-2024
#Revisao: 1_20_09_2024

#----->Instale o StreamLit:
#-->rode por favor pip install streamlit
import streamlit as st

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------>Preparativos para acessar tabelas e o banco de dados MySQL no Python

#----->Instale o MySQL connector, se desejar transformar em
#-->banco de dados a tabela cedida pela professora, pórem use:
#-->rode por favor pip install mysql-connector-python
#-->Dica: rodar pip install mysql-connector é possível,
#-->pode dar erro de caching_sha2_password mesmo se
#-->alterar para mysql_native_password, o Python não
#consegue perceber a mudança
import mysql.connector

from mysql.connector import errorcode

#----->Instale o Pandas, se não o possuir no PC:
#-->rode por favor        
import pandas as pd

#importar as credenciais guardadas do MySQL 
#para instalar: pip install toml 
import toml

#rode pip install os
import os

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------>Preparativos para gerar tabelas e gráficos no Python

#Microsoft Visual C++ 14.0 ou acima é necessário para evitar erros com as
# bibliotecas matplotlib e vega. 
# Ele pode ser obtido a partir do "Microsoft C++ Build Tools": 
# Por gentileza, acesse: https://visualstudio.microsoft.com/visual-cpp-build-tools/

#pip install matplotlib
import matplotlib.pyplot as plt
#ver site: https://www.w3schools.com/python/matplotlib_pyplot.asp
#https://docs.streamlit.io/develop/api-reference/charts

#pip install numpy
import numpy as np

#pip install openpyxl
import openpyxl

#----------------->Estudarei como instalar, as bibliotecas a seguir:
#pip install streamlit-vega-lite
#pip install vega
from streamlit_vega_lite import vega_lite_component, altair_component

#pip install plotly==5.24.0
import plotly.io
#vem junto com plotly
import plotly.figure_factory as ff
#vem junto com plotly
import plotly.express as px

#pip install scipy
import scipy

#pip install vega-datasets
#pip install altair
import altair as alt
#ver site: https://www.datacamp.com/tutorial/altair-in-python

#pip install seaborn #--------------------------->Revisão Gabriel
import seaborn as sns #-------------------------->Revisão Gabriel

#-------------------------------------------------Carregando a base de dados em CSV/Excel/MySQL-------------------------------------------------#
#conexao MySQL:
#criar arquivo de credenciais se não existe, por parâmetros
def generate_toml(host,port,database,username,password,table):
    
    type_sgbd="mysql" #Mudar se necessário 
    
    if isinstance(host, str) and isinstance( port,int) and isinstance(database, str) and isinstance(username, str) and isinstance(password, str) and isinstance(table,str):
        print("Valores Válidos") 
        try:
            with open(".streamlit/secrets.toml","r"):
                print("Arquivo Existe.")
        except:
            try:
                os.mkdir('.streamlit')
                
                #usar se for definir o charset do bay
                start_charset=("""={""")
                mid_charset="charset='"
                type_charset="xxx"
                end_charset=("""'}""")
                
                #texto-base do arquivo de credenciais 
                texto=(f'''
#Criado por: função do Python
#Local: .streamlit/secrets.toml

['{type_sgbd}']
dialect = '{type_sgbd}'
host = '{host}'  #Mudar host se necessario
port = {port}  #Mudar porta se necessario
database = '{database}'  #Mudar banco se necessario
user = '{username}'  #Mudar usario se necessario
password = '{password}'  #Mudar senha se necessario
table='{table}'  #Mudar nome da tabela se necessario

#If you use query when defining your connection, 
#you must use streamlit>=1.35.0.
#query{start_charset}{mid_charset}{type_charset}{end_charset}

                '''
                )
#query = { charset = "xxx" }
                print(texto)
                
                with open(".streamlit/secrets.toml","w", encoding="utf-8") as arquivo:
                    arquivo.write(texto)

            except OSError as os_erro_arquivo:
                print("falha no processo de criação do arquivo.")
                print(os_erro_arquivo)
        
    else:
        print("Valores Inválidos, não são Strings.")    

#Solicitará suas credenciais para leitura inicial e checagem
def get_read_toml():
    
    try:
        with open(".streamlit/secrets.toml","r") as arquivo: 
            print()  
            config = toml.load(arquivo)  
            #Imprimindo todo o arquivo de credenciais(.toml) obtido
            print(config)

            
    except Exception as erro:
        print("Erro encontrado.")  
        print(erro)   

#Realizar conexao MySQL:
def get_from_mysql(HOST,BANCO_MYSQL,SENHA,USUARIO,TABELA_MYSQL):
    #estabelecendo conexão
    try:
        meu_banco = mysql.connector.connect(
          host=HOST,
          user=USUARIO,
          password=SENHA,
          database=BANCO_MYSQL
        )
        print("database online")
        if meu_banco and meu_banco.is_connected():
          with meu_banco.cursor() as cursor:
            #resultado = cursor.execute("SELECT * FROM %s",TABELA_MYSQL)
            sql_select= (f"SELECT * FROM `{BANCO_MYSQL}.{TABELA_MYSQL}`")
            resultado=cursor.execute(sql_select)
            linhas_mysql = resultado.fetchall()
            colunas_mysql= tuple(meu_banco.execute(resultado).keys())
            df = pd.DataFrame(linhas_mysql, columns=colunas_mysql,index=False)
          return df
        else:
          print("Não foi possível obter os dados.")
          return None
    except mysql.connector.Error as erro_conectar:
        if erro_conectar.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Algo está errado com %s ou %s",USUARIO,SENHA)
        elif erro_conectar.errno == errorcode.ER_BAD_DB_ERROR:
          print("%s não existe",BANCO_MYSQL)
        else:
          print(erro_conectar)
        return None
        
#Solicitará suas credenciais e atribuirá a variaveis
def get_from_toml_to_mysql():
    
    #criar arquivo de credenciais se não existe
    generate_toml("localhost",3306,"xxx","xxx","xxx","xxx") 
            #-->  host,porta,database,usuario,senha,tabela 
    
    #verificar se arquivo de credenciais foi criado 
    #e realiza a leitura inicial:
    get_read_toml()

    #verificar se arquivo de credenciais existe:
    try:
      print("Acessando arquivo de crednciais MySQL.....")
      # Lendo dados
      toml_data = toml.load(".streamlit/secrets.toml")
      # salvando cada credencial em uma variável 
      HOST = toml_data['mysql']['host']
      BANCO_MYSQL = toml_data['mysql']['database']
      SENHA = toml_data['mysql']['password']
      USUARIO = toml_data['mysql']['user']
      PORTA =  toml_data['mysql']['port']
      TABELA_MYSQL=toml_data['mysql']['table']
      print("Exibindo arquivo de credenciais MySQL:")
      print(HOST)
      print(BANCO_MYSQL)
      print(SENHA)
      print(USUARIO)
      print(PORTA)
      print(TABELA_MYSQL)
  
      return get_from_mysql(HOST,BANCO_MYSQL,SENHA,USUARIO,TABELA_MYSQL)
    except Exception as erro:
      print("Erro encontrado.")  
      print(erro)
      return None

#cache do streamlit
@st.cache_data 
#st.cache_resource

#se CSV:
def data_upload_csv():
  df=pd.read_csv("../Dataset salary 2024.csv")
  return df

#se Excel:
def data_upload_excel():
  df=pd.read_excel("../Dataset salary 2024.xlsx")
  return df


#se MySQL:
def data_upload_mysql():
  return get_from_mysql()
   
#---------------------------------------------------------Executando as questões----------------------------------------------------------------#
#---------------------------------------------------------------Questão 1-----------------------------------------------------------------------#
def quest_1():
  st.write("""Questão 1\n
  Construa uma tabela de frequências,\n 
  de forma adequada, para representar\n 
  a variável salário_in_usd.\n
  (não finalizado)""")
  
  # Se Excel:
  df2 = data_upload_excel()
  
  # Calcular o número de faixas (k) usando a Regra de Sturges, sendo n o tamanho da amostra
  n = len(df2['salary_in_usd'])  
  k = int(1 + 3.322 * np.log10(n))
  
  # Determinar o menor e o maior valor da coluna salary_in_usd
  menor_valor = df2['salary_in_usd'].min()
  maior_valor = df2['salary_in_usd'].max()
  
  # Definir os limites das faixas manualmente
  faixas = np.linspace(menor_valor, maior_valor, k + 1)
  
  # Definir as faixas de salários
  faixas_salario = pd.cut(df2['salary_in_usd'], bins=faixas, include_lowest=True)
  
  # Calcular as frequências
  frequencia = faixas_salario.value_counts(sort=False)
  percentual = frequencia / frequencia.sum() * 100
  freq_acumulada = frequencia.cumsum()
  perc_acumulada = percentual.cumsum()

  # Extrair os limites inferiores e superiores das faixas
  limites_inferiores = [interval.left for interval in faixas_salario.cat.categories]
  limites_superiores = [interval.right for interval in faixas_salario.cat.categories]

  # Construir a coluna com as faixas de salário
  faixas = [f"{inf} |-- {sup}" for inf, sup in zip(limites_inferiores, limites_superiores)]

  # Construir o DataFrame com as colunas necessárias
  dist_freq = pd.DataFrame({
      'Faixas de Salário (USD)': faixas,  # Nome personalizado para as faixas
      'Frequência Absoluta': frequencia.values,  # Garantindo apenas os valores
      'Frequência Relativa (%)': percentual.values,
      'Frequência Absoluta Acumulada': freq_acumulada.values,
      'Frequência Relativa Acumulada (%)': perc_acumulada.values
  })

  # Adicionar a linha "Total"
  total_frequencia_absoluta = frequencia.sum()
  total_frequencia_relativa = 100.0
  dist_freq.loc[len(dist_freq)] = ['Total', total_frequencia_absoluta, total_frequencia_relativa, '', '']

  # Exibir a tabela de frequências no Streamlit
  st.dataframe(data=dist_freq, use_container_width=True)



#---------------------------------------------------------------Questão 2-----------------------------------------------------------------------#
def quest_2():
  st.write("""Questão 2\n
  Construa uma tabela de frequências,\n 
  de forma adequada, para representar\n 
  a variável job_title.\n
  (não finalizado)""")
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  frequencia = df2['job_title'].value_counts()
  percentual = df2['job_title'].value_counts(normalize = True)*100
 
  #Construímos o DataFrame com a frequência 
  #e o percentual:
  dist_freq_qualitativas = pd.DataFrame({'Frequência': frequencia, 'Porcentagem(%)': percentual})

  #Modelo 1
  #exibindo a tabela de frequências
  #Jobs = df2.groupby(['job_title'])['job_title'].count().reset_index( 
  #name='Count').sort_values(['Count']) 
  #st.dataframe(data=Jobs,hide_index=True)

  #teste 
  #Modelo 2(em uso)
  #exibindo a tabela de frequências
  st.dataframe(data=dist_freq_qualitativas,
    column_config={
        "widgets": st.column_config.Column(
            width="medium"
        )
    },use_container_width=True
  )
#-----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------->Preparativos Questão 3
#------------------------------>Qualitativos(podem ser unidos por similaridade)
def get_3_a():
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()
  
  quest_3_plot_1=df2['experience_level']   
  frequencia_1 = quest_3_plot_1.value_counts().sort_values(ascending=True)
  percentual_1 = quest_3_plot_1.value_counts(normalize = True)*100

  #Construímos o DataFrame com a frequência 
  #e o percentual:
  dist_freq_quantitativas_1 = pd.DataFrame({'Frequência': frequencia_1, 'Porcentagem(%)': percentual_1})
  st.write('experience_level - analise')
  #Opções em subtópicos
  subtopic_graph=st.selectbox(
                          'Tabelas e Gráficos',
                          ['Selecione uma opção',
                          'Tabela de Frequência',
                          'Gráfico de Barras'])
  if subtopic_graph == 'Selecione uma opção':
     st.write("Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico.")
  elif subtopic_graph == 'Tabela de Frequência':
    #Exibe a tabela
    st.write('experience_level - Tabela de Frequência')
    st.dataframe(dist_freq_quantitativas_1,
      column_config={
          "widgets": st.column_config.Column(
              width="medium"
          )
      },use_container_width=True
    )
#----------------> 
  elif subtopic_graph == 'Gráfico de Barras':
    #Exibe o Gráfico de Barras
    st.write('experience_level - Gráfico de Barras')
    st.bar_chart(dist_freq_quantitativas_1)
#----------------> 

def get_3_b():
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()
  
  quest_3_plot_2=df2['employment_type']  
  frequencia_2 = quest_3_plot_2.value_counts().sort_values(ascending=True)
  percentual_2 = quest_3_plot_2.value_counts(normalize = True)*100

  #Construímos o DataFrame com a frequência 
  #e o percentual:
  dist_freq_quantitativas_2 = pd.DataFrame({'Frequência': frequencia_2, 'Porcentagem(%)': percentual_2})
  st.write('employment_type - analise')
  #Opções em subtópicos
  subtopic_graph=st.selectbox(
                          'Tabelas e Gráficos',
                          ['Selecione uma opção',
                          'Tabela de Frequência',
                          'Gráfico de Barras',
                          'Gráfico de Barras v2'])  #-------------------------->Revisão Gabriel
  if subtopic_graph == 'Selecione uma opção':
     st.write("Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico.")
  elif subtopic_graph == 'Tabela de Frequência':
    #Exibe a tabela
    st.write('employment_type- Tabela de Frequência') 
    st.dataframe(dist_freq_quantitativas_2,
      column_config={
          "widgets": st.column_config.Column(
              width="medium"
          )
      },use_container_width=True
    )
#----------------> 
  elif subtopic_graph == 'Gráfico de Barras':
    #Exibe o Gráfico de Barras
    st.write('employment_type- Gráfico de Barras')
    st.bar_chart(dist_freq_quantitativas_2)

#------------------------------------------>Revisão Gabriel - Inicio 
  elif subtopic_graph == 'Gráfico de Barras v2':
    #Exibe o Gráfico de Barras
    
    st.write('experience_level - Gráfico de Barras v2')
    
    teste=sns.barplot(x=percentual_1.index,             # `y` recebe o conjunto de valores que correspondem ao eixo x.
            y=frequencia_1,               # `y` recebe o conjunto de valores que correspondem ao eixo y.
            color="blue",                    # `color` recebe uma string com o nome de uma cor para as barras.
            label='Qtd.')                     # `label` será o "nome" que este gráfico receberá, utilizaremos este "nome" para
                                             # gerar uma legenda para nosso gráfico.
    plt.title('experience_level\nGráfico de Barras v2')         # Adiciona título ao gráfico
    plt.ylabel('Frequência')                     # Adiciona um rótulo ao eixo y
    plt.xlabel('Quantidade')                     # Adiciona um rótulo ao eixo x
    plt.legend()
    # Display the plot in Streamlit
    st.pyplot(teste.figure)
#------------------------------------------>Revisão Gabriel - Fim
  
def get_3_c():
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()
  
  quest_3_plot_3=df2['company_size'] 
  st.write('company_size - analise') 
  frequencia_3 = quest_3_plot_3.value_counts().sort_values(ascending=True)
  percentual_3 = quest_3_plot_3.value_counts(normalize = True)*100

  #Construímos o DataFrame com a frequência 
  #e o percentual:
  dist_freq_quantitativas_3 = pd.DataFrame({'Frequência': frequencia_3, 'Porcentagem(%)': percentual_3})
  #Opções em subtópicos
  subtopic_graph=st.selectbox(
                          'Tabelas e Gráficos',
                          ['Selecione uma opção',
                          'Tabela de Frequência',
                          'Gráfico de Barras'])
  if subtopic_graph == 'Selecione uma opção':
     st.write("Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico.")
  elif subtopic_graph == 'Tabela de Frequência':
    #Exibe a tabela
    st.write('company_size- Tabela de Frequência') 
    st.dataframe(dist_freq_quantitativas_3,
      column_config={
          "widgets": st.column_config.Column(
              width="medium"
          )
      },use_container_width=True
    )
#----------------> 
  elif subtopic_graph == 'Gráfico de Barras':
    st.write('company_size - Gráfico de Barras')
    #Exibe o Gráfico de Barras
    st.bar_chart(dist_freq_quantitativas_3) 

#------------------------------>Quantitativos(podem ser unidos por similaridade)
def get_3_d():
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()
  
  quest_3_plot_4=df2['salary_in_usd']  
  st.write('salary_in_usd - analise')
  frequencia_4 = quest_3_plot_4.value_counts().sort_values(ascending=True)
  percentual_4 = quest_3_plot_4.value_counts(normalize = True)*100

  #Construímos o DataFrame com a frequência 
  #e o percentual:
  dist_freq_quantitativas_4 = pd.DataFrame({'Frequência': frequencia_4, 'Porcentagem(%)': percentual_4})
  #Opções em subtópicos
  subtopic_graph=st.selectbox(
                          'Tabelas e Gráficos',
                          ['Selecione uma opção',
                          'Tabela de Frequência',
                          'Gráfico de Barras',
                          'Gráfico de Linhas',
                          'Gráfico Historigrama'])
  if subtopic_graph == 'Selecione uma opção':
     st.write("Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico.")
  elif subtopic_graph == 'Tabela de Frequência':
    #Exibe a tabela
    st.write('salary_in_usd - Tabela de Frequência')  
    st.dataframe(dist_freq_quantitativas_4,
      column_config={
          "widgets": st.column_config.Column(
              width="medium"
          )
      },use_container_width=True
    )
#----------------> 
  elif subtopic_graph == 'Gráfico de Barras':
    #Exibe o Gráfico de Barras
    st.write('salary_in_usd - Gráfico de Barras')
    st.bar_chart(dist_freq_quantitativas_4) 
#---------------->  
  elif subtopic_graph == 'Gráfico de Linhas':
    st.write('salary_in_usd - Gráfico de Linhas')
    #Exibe o Gráfico de Linhas
    fig4 = plt.figure() 
    plt.plot(quest_3_plot_4) 
    st.pyplot(fig4)
#---------------->
  elif subtopic_graph == 'Gráfico Historigrama':
    #Em analise do melhor modelo
    st.write('salary_in_usd - Gráfico Historigrama 1') 
    fig, ax = plt.subplots()
    ax.hist(quest_3_plot_4, bins=500)
    st.pyplot(fig)
    
#---------------->

def get_3_e():
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()
  
  quest_3_plot_5=df2['remote_ratio']    
  st.write('remote_ratio - analise')
  frequencia_5 = quest_3_plot_5.value_counts()
  percentual_5 = quest_3_plot_5.value_counts(normalize = True)*100
  #Construímos o DataFrame com a frequência 
  #e o percentual:
  dist_freq_quantitativas_5 = pd.DataFrame({'Frequência': frequencia_5, 'Porcentagem(%)': percentual_5})

  #Opções em subtópicos
  subtopic_graph=st.selectbox(
                          'Tabelas e Gráficos',
                          ['Selecione uma opção',
                          'Tabela de Frequência',
                          'Gráfico de Barras'])
  if subtopic_graph == 'Selecione uma opção':
     st.write("Ao escolher uma opção, será carregado os gráficos ou tabelas deste tópico.")
  elif subtopic_graph == 'Tabela de Frequência':
    #Exibe a tabela
    st.write('remote_ratio - Tabela de Frequência')
    st.dataframe(dist_freq_quantitativas_5,
      column_config={
          "widgets": st.column_config.Column(
              width="medium"
          )
      },use_container_width=True
    )
  elif subtopic_graph == 'Gráfico de Barras':
    #Exibe o Gráfico de Barras
    st.write('remote_ratio - Gráfico de Barras')
    st.bar_chart(dist_freq_quantitativas_5) 
#---------------->




#---------------------------------------------------------------Questão 3-----------------------------------------------------------------------#
def quest_3():
  st.write("""Questão  3\n 
Construir um gráfico adequado para cada uma das seguintes variáveis:\n 
```
• experience_level             • Employment_type            • salary_in_usd\n
• remote_ratio                 • company_size\n
```           
Escreva um pequeno parágrafo citando os principais achados observados nos gráficos construídos.""")
  parts_quest_3()#Para exibir por partes cada tópico  


#Exibe por partes cada tópico  
def parts_quest_3():
   
#Opções dos tópicos
  graph_project=st.selectbox(
                          'Analises',
                          ['Selecione uma opção',
                          'experience_level',
                          'employment_type',
                          'company_size',
                          'salary_in_usd',
                          'remote_ratio'])
  if graph_project == 'Selecione uma opção':
     st.write("Ao escolher uma opção, será carregado o tópico desejado.")
  elif graph_project == 'experience_level':
    get_3_a()
  elif graph_project == 'employment_type':
    get_3_b()
  elif graph_project == 'company_size':
    get_3_c()
  elif graph_project == 'salary_in_usd':
    get_3_d()
  elif graph_project == 'remote_ratio':
    get_3_e()

#---------------------------------------------------------------Questão 4-----------------------------------------------------------------------#
def quest_4():
  st.write("""Questão 4\n 
Calcule as medidas descritivas (média, mediana, mínimo, máximo, desvio padrão, coeficiente 

\n de variação, 1º quartil, 3º quartil) para a variável salário_in_usd. Construir um boxplot para a variável 

\n salário_in_usd. Escreva um pequeno parágrafo citando as principais informações obtidas por meio da 

\nanálise das medidas descritivas calculadas e do gráfico construído.""")
  #subtópicos da questão
  quest_4_topics()

def quest_4_topics():
  
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  #Construir boxplot
  # Calcular a média aritmétia, mediana, variância e desvio-padrão
  salary=df2['salary_in_usd']
  # média, 
  media = salary.mean()
  # mediana, 
  mediana = salary.median()
  # mínimo, 
  minimo=salary.min()
  # máximo,
  maximo=salary.max() 
  # desvio padrão, 
  desv_pad = np.std(salary)
  # coeficiente de variação,
  variancia = np.var(salary) 
  # 1º quartil, 
  q1 = salary.quantile(.25)
  # 3º quartil
  q3 = salary.quantile(.75)
  
  #Mostrar os resultados  
  st.write('Mostrando tabela com os resultados:')
  columns_r=['Média', 'Mediana','Mínimo','Máximo','Desvio Padrão','Variância','1º quartil','3º quartil']
  lines=[media, mediana,minimo,maximo,desv_pad,variancia,q1,q3]
  results=pd.DataFrame({'Medidas': columns_r, 'Resultados': lines})
  # Plotar Boxplot
  st.dataframe(results,hide_index=True)
  st.write('salary_in_usd - Gráfico Boxplot') 
  #Criando figura
  fig = px.box(salary)
  st.plotly_chart(fig)
#---------------------------------------------------------------Questão 5-----------------------------------------------------------------------#
def quest_5():
  st.write("""Questão 5\nConstruir uma tabela de contingência mostrando a frequência e um dos percentuais (da linha, 
\n da coluna OU do total geral) entre as variáveis experience_level e remote_ratio. Construa um gráfico 

\n adequado para representar os dados dessa tabela. Escreva um pequeno parágrafo citando os 

\n principais achados.""")
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  #fonte: acesse o site a seguir 
  #https://acervolima.com/tabela-de-contingencia-em-python/
  #2 variáveis 
  merge_crosstab = pd.crosstab(df2['experience_level'],
                            df2['remote_ratio'], 
                               margins = True,
                               margins_name="Total")

  st.write('experience_level x remote_ratio - Valores')
  st.dataframe(merge_crosstab)
  merge_crosstab2 = pd.crosstab(df2['experience_level'],
                            df2['remote_ratio'], 
                               margins = True,
                               margins_name="Total",normalize="all").mul(100).round(1)
  st.write('experience_level x remote_ratio - porcentagem')
  st.dataframe(merge_crosstab2)
  st.write('experience_level x remote_ratio - Gráfico de Barras')
  merge_crosstab3 = pd.crosstab(df2['experience_level'],
                               df2['remote_ratio'],  
                               margins = False)
  st.bar_chart(merge_crosstab3,x_label="experience_level",y_label="remote_ratio")

#---------------------------------------------------------------Questão 6-----------------------------------------------------------------------#
def quest_6():
  st.write("""Questão 6 \n
  Construir uma tabela de contingência mostrando a frequência e um dos percentuais (da linha, 

\n da coluna OU do total geral) entre as variáveis Employment_type e company_size. Construa um gráfico 

\n adequado para representar os dados dessa tabela. Escreva um pequeno parágrafo citando os 

\n principais achados.""")
#Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  #fonte: acesse o site a seguir 
  #https://acervolima.com/tabela-de-contingencia-em-python/
  #2 variáveis 
  merge_crosstab = pd.crosstab(df2['employment_type'],
                               df2['company_size'], 
                               margins = True,
                               margins_name="Total")
  st.write('employment_type x company_size - Valores')
  st.dataframe(merge_crosstab)
  merge_crosstab2 = pd.crosstab(df2['employment_type'],
                               df2['company_size'],  
                               margins = True,
                               margins_name="Total",normalize="all").mul(100).round(1)
  st.write('employment_type x company_size - porcentagem')
  st.dataframe(merge_crosstab2)
  st.write('employment_type x company_size - Gráfico de Barras')
  merge_crosstab3 = pd.crosstab(df2['employment_type'],
                               df2['company_size'],  
                               margins = False)
  st.bar_chart(merge_crosstab3,x_label="employment_type",y_label="company_size")


#---------------------------------------------------------------Questão 7-----------------------------------------------------------------------#
def quest_7():
  st.write("""Questão 7\n
  Calcule as medidas descritivas (média, mediana, mínimo, máximo, desvio padrão, coeficiente 

\n de variação, 1º quartil, 3º quartil) para a variável salário_in_usd estratificando pela variável

\n experience_level. Construir um boxplot estratificado entre essas duas variáveis. Escreva um pequeno 

\n parágrafo citando as principais informações obtidas por meio da análise das medidas descritivas 

calculadas e do gráfico construído (compare as medianas, a variabilidade, a homogeneidade, a 

\n presença de valores discrepantes e as médias).""")
#Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  merge_crosstab = pd.crosstab(df2['salary_in_usd'],
                                df2['experience_level'],  
                                margins = False)

  salary=merge_crosstab
  # média, 
  media = salary.mean()
  
  st.write('média: ', media)
  # mediana, 
  mediana = salary.median()

  st.write('mediana: ', mediana)
  # mínimo, 
  minimo=salary.min()

  st.write('mínimo: ', minimo)
  # máximo,
  maximo=salary.max()

  st.write('máximo: ', maximo)
  # desvio padrão, 
  desv_pad = np.std(salary)

  st.write('desvio padrão: ', desv_pad)
  # coeficiente de variação,
  variancia = np.var(salary) 

  st.write('coeficiente de variação: ', variancia)
  # 1º quartil, 
  q1 = salary.quantile(.25)
  q1.columns=['1º quartil']
  st.write('1º quartil', q1)
  # 3º quartil
  q3 = salary.quantile(.75)
  
  st.write('3º quartil', q3)
  
  #Mostrar os resultados  
  st.write('Mostrando os resultados como tabela:')
  columns_r=['Média', 'Mediana','Mínimo','Máximo','Desvio Padrão','Variância','1º quartil','3º quartil']
  m=pd.concat([media, mediana,minimo,maximo,desv_pad,variancia,q1,q3],axis=1,keys=columns_r)
  st.dataframe(m)
  st.write('Mostrando os resultados como Boxplot:')
  fig = px.box(m)
  st.plotly_chart(fig)
#---------------------------------------------------------------Questão 8-----------------------------------------------------------------------#
def quest_8():
  st.write("""Questão 8\n
Calcule as medidas descritivas (média, mediana, mínimo, máximo, desvio padrão, coeficiente 

de variação, 1º quartil, 3º quartil) para a variável salário_in_usd estratificando pela variável 

Employment_type. Construir um boxplot estratificado entre essas duas variáveis. Escreva um pequeno 

parágrafo citando as principais informações obtidas por meio da análise das medidas descritivas 

calculadas e do gráfico construído (compare as medianas, a variabilidade, a homogeneidade, a 

presença de valores discrepantes e as médias).""")
#Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()

  merge_crosstab = pd.crosstab(df2['salary_in_usd'],
                                df2['employment_type'],  
                                margins = False)

  salary=merge_crosstab
  # média, 
  media = salary.mean()
  st.write('média: ', media)
  # mediana, 
  mediana = salary.median()
  st.write('mediana: ', mediana)
  # mínimo, 
  minimo=salary.min()
  st.write('mínimo: ', minimo)
  # máximo,
  maximo=salary.max() 
  st.write('máximo: ', maximo)
  # desvio padrão, 
  desv_pad = np.std(salary)
  st.write('desvio padrão: ', desv_pad)
  # coeficiente de variação,
  variancia = np.var(salary) 
  st.write('coeficiente de variação: ', variancia)
  # 1º quartil, 
  q1 = salary.quantile(.25)
  st.write('1º quartil', q1)
  # 3º quartil
  q3 = salary.quantile(.75)
  st.write('3º quartil', q3)
  
  #Mostrar os resultados  
  st.write('Mostrando os resultados como tabela:')
  columns_r=['Média', 'Mediana','Mínimo','Máximo','Desvio Padrão','Variância','1º quartil','3º quartil']
  m=pd.concat([media, mediana,minimo,maximo,desv_pad,variancia,q1,q3],axis=1,keys=columns_r)
  st.dataframe(m)
  st.write('Mostrando os resultados como Boxplot:')
  fig = px.box(m)
  st.plotly_chart(fig)



#---------------------------------------------------------------Questão 9-----------------------------------------------------------------------#
def quest_9():
  st.write("""Questão 9\n
Cite uma situação hipotética em que o gráfico de linhas seria adequado para representar tais 

\n dados. Quais informações podemos obter ao utilizar um gráfico de linhas?""")





#---------------------------------------------------------------Questão 10----------------------------------------------------------------------#

def quest_10():
  st.write("""Questão 10
\n Pesquise a respeito do uso de mapa de calor em tabelas. Quando ele deve ser usado? Qual sua 

\n utilidade/benefícios? Mostre um exemplo hipotético.""")



#------------------------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------Organizando o Front-End------------------------------------------------------------------#
#----------------->Executando Streamlit 
def load_descricao():
  st.write("Engenharia de Computação - Campus Coração Eucarístico")
  st.write("PMG - Noite - G1/T1 - 2024/2")
  st.write("Trabalho desenvolvido para a matéria:")
  st.write("Estatítica e Probabilidade")
  st.write("Turma 82.27.101")
  st.write("Professor(a) responsável: Julienne Borges Fujii")
  st.write("Alunos: Bruno Henrique Reis Almeida")
  st.write("Gabriel da Silva Cassino")
  st.write("Tema Proposto:")
  st.write("Salário do desenvolvedor de dados em 2024")
  st.write("Analisando salários de desenvolvedores de dados em 2024") 


def load_planilha_excel():
  st.write("Planilha cedida pela professora Julienne Borges Fujii")
  
  #Se CSV:
  #df1=data_upload_csv()
  #Se Excel:
  df2=data_upload_excel()
  #ou MySQL:
  #df3=data_upload_mysql()


  #escolha conforme desejar: df1,df2 ou df3(abaixo é apenas um exemplo)
  st.dataframe(data=df2)

#Menu Inicial
def main_page():
  st.sidebar.title('Menu')
  Page_Project=st.sidebar.selectbox(
                          'Questões',
                          ['Descrição',
                          'Planilha Excel',
                          'Questão 1',
                          'Questão 2',
                          'Questão 3',
                          'Questão 4',
                          'Questão 5',
                          'Questão 6',
                          'Questão 7',
                          'Questão 8',
                          'Questão 9',
                          'Questão 10'])
  
  if Page_Project == 'Descrição':
    load_descricao()
  elif Page_Project == 'Planilha Excel':
    load_planilha_excel()  
  elif Page_Project == 'Questão 1':
    quest_1()
  elif Page_Project == 'Questão 2':
    quest_2() 
  elif Page_Project == 'Questão 3':
    quest_3() 
  elif Page_Project == 'Questão 4':
    quest_4() 
  elif Page_Project == 'Questão 5':
    quest_5()   
  elif Page_Project == 'Questão 6':
    quest_6() 
  elif Page_Project == 'Questão 7':
    quest_7() 
  elif Page_Project == 'Questão 8':
    quest_8() 
  elif Page_Project == 'Questão 9':
    quest_9() 
  elif Page_Project == 'Questão 10':
    quest_10()     

#rode no terminal: streamlit run main.py

#criar arquivo de credenciais MySQL, se for usar banco de dados
#Passe os parãmetros para a função conforme for o seu banco de dados
#generate_toml('localhost',3306,'database','username','password','table')

#carrega a base no front-end, acesso o navegador no IP e Porta fornecidos no terminal
main_page()
