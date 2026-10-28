import pandas as pd, numpy as np, re
SRC='AI_Usage_and_Impact_on_Students_and_Professionals.csv'
raw=pd.read_csv(SRC)
log={'filas_originales':len(raw)}
df=raw.drop_duplicates().copy()
log['duplicados_exactos_eliminados']=len(raw)-len(df)
df=df.drop_duplicates(subset='User_ID',keep='first')
log['filas_tras_limpieza']=len(df)

def num(s):
    return pd.to_numeric(s.astype(str).str.extract(r'(-?\d+\.?\d*)')[0],errors='coerce')
for c in ['Age','Monthly_Income','AI_Usage_Hours_Per_Day','Time_Saved_Hours_Per_Week','Work_or_Study_Hours_Per_Day','Monthly_AI_Cost']:
    df[c]=num(df[c])

g=df.Gender.str.strip().str.lower()
df['Genero']=g.map({'male':'Hombre','m':'Hombre','female':'Mujer','f':'Mujer','other':'Otro','non-binary':'Otro'})

c=df.Country.str.strip().str.lower()
cm={'united states':'Estados Unidos','united states of america':'Estados Unidos','u.k.':'Reino Unido','united kingdom':'Reino Unido',
 'india':'India','canada':'Canadá','pakistan':'Pakistán','philippines':'Filipinas','brazil':'Brasil','australia':'Australia',
 'nigeria':'Nigeria','germany':'Alemania','france':'Francia','kenya':'Kenia'}
df['Pais']=c.map(cm)

e=df.Education_Level.str.strip().str.lower()
def edu(x):
    if pd.isna(x): return np.nan
    if x in('high school','hs'): return 'Secundaria'
    if x in('diploma',): return 'Diploma'
    if x in('undergraduate','undergrad'): return 'Pregrado en curso'
    if x.startswith('bachelor') or x=='ba/bsc': return 'Licenciatura'
    if x.startswith('master') or x=='ma/msc': return 'Maestría'
    if x in('phd','ph.d.'): return 'Doctorado'
    return np.nan
df['Educacion']=e.map(edu)

t=df.AI_Tool.str.strip().str.lower()
tm={'chatgpt':'ChatGPT','chat gpt':'ChatGPT','google gemini':'Gemini','gemini':'Gemini','microsoft copilot':'Copilot','copilot':'Copilot',
 'claude':'Claude','perplexity ai':'Perplexity','grammarly':'Grammarly','meta ai':'Meta AI','deepseek':'DeepSeek'}
df['Herramienta']=t.map(tm)

pm={'Coding':'Programación','Writing':'Escritura','Studying':'Estudio','Research':'Investigación','Content Creation':'Creación de contenido',
 'Data Analysis':'Análisis de datos','Customer Support':'Atención al cliente','Office Work':'Trabajo de oficina'}
df['Proposito']=df.AI_Purpose.map(pm)
df['Tipo_Usuario']=df.User_Type.map({'Student':'Estudiante','Professional':'Profesional'})

def area(p):
    if pd.isna(p): return np.nan
    s=p.lower()
    rules=[('Atención al cliente',['customer','support','kundenservice','kundenbetreuerin','atendimento','atención']),
     ('Datos y analítica',['data','dados','analyst','analista','analytics','statistic','business intelligence','machine learning','artificial intelligence','inteligência artificial','pesquisador de mercado']),
     ('Tecnología y software',['software','developer','desenvolved','développeur','web','computer','information technology','engenheiro de software','full stack','tech lead']),
     ('Contenido y marketing',['content','contenu','marketing','social media','media','writer','blog','creator','communications','strateg']),
     ('Literatura y humanidades',['literature','creative writing','history','english']),
     ('Ciencias e investigación',['research','biology','bioinformatics','biomedical science','psychology','mathematics','biotech','physics','scientist','environmental','molecular','technician','lab','chem']),
     ('Ingeniería',['engineering','engineer','mechanical']),
     ('Negocios y administración',['business','administrat','manager','assistant','finance','account','hr','sales'])]
    for name,keys in rules:
        if any(k in s for k in keys): return name
    return 'Otros'
df['Area']=df.Profession.map(area)

# outliers imposibles
log['uso_diario_>16h_a_NaN']=int((df.AI_Usage_Hours_Per_Day>16).sum()); df.loc[df.AI_Usage_Hours_Per_Day>16,'AI_Usage_Hours_Per_Day']=np.nan
log['trabajo_estudio_>16h_a_NaN']=int((df.Work_or_Study_Hours_Per_Day>16).sum()); df.loc[df.Work_or_Study_Hours_Per_Day>16,'Work_or_Study_Hours_Per_Day']=np.nan
log['edad_>90_a_NaN']=int((df.Age>90).sum()); df.loc[df.Age>90,'Age']=np.nan
log['ingreso_>50000_marcado']=int((df.Monthly_Income>50000).sum())
df['Ingreso_atipico']=df.Monthly_Income>50000
df['Horas_IA_Semana']=df.AI_Usage_Hours_Per_Day*7
df['Ahorro_por_hora_IA']=df.Time_Saved_Hours_Per_Week/df.Horas_IA_Semana
df['Paga']=np.where(df.Monthly_AI_Cost.isna(),np.nan,(df.Monthly_AI_Cost>0).astype(float))
df=df.rename(columns={'Monthly_AI_Cost':'Costo_mensual_USD','Monthly_Income':'Ingreso_mensual','Productivity_Score':'Productividad','Accuracy_Rating':'Precision','Satisfaction_Score':'Satisfaccion','Time_Saved_Hours_Per_Week':'Horas_ahorradas_semana','AI_Usage_Hours_Per_Day':'Horas_IA_dia','Work_or_Study_Hours_Per_Day':'Horas_trabajo_estudio_dia','Age':'Edad','Would_Recommend':'Recomendaria'})
df['Recomendaria']=df.Recomendaria.map({'Yes':'Sí','No':'No','Maybe':'Quizás'})
for col in ['Genero','Pais','Educacion','Herramienta','Proposito','Area']:
    log['nulos_'+col]=int(df[col].isna().sum())
cols=['User_ID','Edad','Genero','Pais','Tipo_Usuario','Educacion','Profession','Area','Ingreso_mensual','Ingreso_atipico','Herramienta','Proposito','Horas_IA_dia','Horas_IA_Semana','Costo_mensual_USD','Paga','Productividad','Precision','Satisfaccion','Horas_ahorradas_semana','Ahorro_por_hora_IA','Horas_trabajo_estudio_dia','Recomendaria']
df=df[cols].rename(columns={'Profession':'Profesion'})
df.to_csv('datos_limpios.csv',index=False)
import json;json.dump(log,open('log_limpieza.json','w'),indent=1,ensure_ascii=False)
print(log)
print(df.Area.value_counts(dropna=False))
print(df[df.Area=='Otros'].Profesion.unique())
print(df.isna().sum())
