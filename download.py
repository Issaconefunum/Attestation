import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly
import plotly.express as px
from scipy import stats
from scipy.stats import mannwhitneyu

def varibility(variable):
    if ((len(dataframe[variable]) /2) > len(dataframe[variable].unique())):
        dub = dataframe.groupby(dataframe[variable].tolist(), as_index= False). size ()
        fig = px.pie(dub, names ='index', values ='size')
        return fig
    else:
        fig = px.scatter(dataframe, x=variable)
        return fig

uploaded_file = st.file_uploader("Choose a file")
#dataframe = pd.read_csv("ground_water_quality_2018_post.csv")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    try:
        dataframe = pd.read_csv(uploaded_file)
    except:
        st.write('Невозможно провести анализ данного файла. Пожалуйста, загрузите .cvs файл')
        st.stop()
    df = dataframe.columns.values.tolist()
    
    variable1 = st.selectbox('variable 1', df, key='1') #выбор переменных
    st.plotly_chart(varibility(variable1))
    
    variable2 = st.selectbox('variable 2', df)
    st.plotly_chart(varibility(variable2))
    
    st.write('Имеем Н0 гипотезу«Данные взаимосвязаны между собой»')
    name_test = ['t-test', 'U-test'] #Выбор теста и исполнение 
    test = st.selectbox('test', name_test)
    try:
        if test == 't-test':
            res = stats.ttest_ind(dataframe[variable1], 
                                  dataframe[variable2],
                                  equal_var=False)
            pvalue = res.pvalue / 2 
            st.write(f'p-value for single sided test: {res.pvalue / 2:.4f}')
        elif test == 'U-test':
            _, pvalue = mannwhitneyu(dataframe[variable1], dataframe[variable2])
        if pvalue >= 0.05:
            st.write(f'Утверждение неверно, pvalue = {pvalue}')
        else:
            st.write(f'Норм, pvalue = {pvalue}')
    except:
        st.write('Невозможно сравнить категориальный тип')
else:
    st.write('Пустой файл')
    