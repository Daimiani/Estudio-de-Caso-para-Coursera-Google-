import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130,'axes.titleweight':'bold','axes.titlesize':12})
OUT='graficos/'
AZ='#2F5D8A'; NA='#E07B39'; VE='#4C9F70'; GR='#9AA5B1'
df=pd.read_csv('datos_limpios.csv')
c=df.dropna(subset=['Costo_mensual_USD'])
def barh(ax,s,color=AZ,fmt='{:.0f}',title='',xlabel='',sort=True):
    if sort: s=s.sort_values()
    b=ax.barh(s.index,s.values,color=color)
    for r,v in zip(b,s.values): ax.text(v+s.max()*0.01,r.get_y()+r.get_height()/2,fmt.format(v),va='center',fontsize=9)
    ax.set_title(title,loc='left'); ax.set_xlabel(xlabel); ax.set_xlim(0,s.max()*1.15)
def fig_pair(name,by,title,label_total='Gasto total mensual (USD)'):
    d=c.dropna(subset=[by]); g=d.groupby(by).Costo_mensual_USD
    tot=g.sum(); med=g.mean()
    fig,ax=plt.subplots(1,2,figsize=(11,max(3.6,0.45*len(tot)+1.5)))
    barh(ax[0],tot,AZ,'${:,.0f}',label_total if False else 'Gasto total mensual',"USD / mes (suma de la muestra)")
    barh(ax[1],med.reindex(tot.sort_values().index),NA,'${:.1f}','Gasto medio por usuario','USD / mes por usuario',sort=False)
    ax[1].set_yticklabels([])
    fig.suptitle(title,x=0.01,ha='left',fontsize=13,fontweight='bold'); fig.tight_layout(); fig.savefig(OUT+name,bbox_inches='tight'); plt.close()
fig_pair('01_gasto_herramienta.png','Herramienta','Gasto mensual en IA por herramienta')
fig_pair('02_gasto_profesion.png','Area','Gasto mensual en IA por área de profesión')
fig_pair('03_gasto_proposito.png','Proposito','Gasto mensual en IA por propósito de uso')
fig_pair('04_gasto_educacion.png','Educacion','Gasto mensual en IA por nivel educativo')
fig_pair('05_gasto_tipo.png','Tipo_Usuario','Gasto mensual en IA: estudiantes vs profesionales')

# 06 pagadores por herramienta
g=c.dropna(subset=['Herramienta']).groupby('Herramienta')
pct=g.Paga.mean()*100; pay=c[c.Paga==1].groupby('Herramienta').Costo_mensual_USD.mean()
fig,ax=plt.subplots(1,2,figsize=(11,3.8))
barh(ax[0],pct,VE,'{:.0f}%','% de usuarios que paga','% de usuarios con costo > 0')
barh(ax[1],pay.reindex(pct.sort_values().index),NA,'${:.1f}','Ticket medio entre quienes pagan','USD / mes',sort=False); ax[1].set_yticklabels([])
fig.suptitle('Quién paga y cuánto paga, por herramienta',x=0.01,ha='left',fontsize=13,fontweight='bold'); fig.tight_layout(); fig.savefig(OUT+'06_pagadores_herramienta.png',bbox_inches='tight'); plt.close()

# 07 distribución de planes
fig,ax=plt.subplots(figsize=(7,3.6))
vc=c.Costo_mensual_USD.value_counts().sort_index()
b=ax.bar([f'${int(i)}' for i in vc.index],vc.values,color=AZ)
for r,v in zip(b,vc.values): ax.text(r.get_x()+r.get_width()/2,v+2,f'{v} ({v/len(c):.0%})',ha='center',fontsize=9)
ax.set_title('Distribución del costo mensual declarado',loc='left'); ax.set_ylabel('Usuarios'); ax.set_xlabel('Costo mensual')
fig.tight_layout(); fig.savefig(OUT+'07_distribucion_costos.png',bbox_inches='tight'); plt.close()

# 08 uso semanal por herramienta / área / propósito / educación / tipo
u=df.dropna(subset=['Horas_IA_Semana'])
fig,ax=plt.subplots(2,2,figsize=(11,8))
for a,(by,t) in zip(ax.flat,[('Herramienta','Por herramienta'),('Area','Por área de profesión'),('Proposito','Por propósito'),('Educacion','Por nivel educativo')]):
    barh(a,u.dropna(subset=[by]).groupby(by).Horas_IA_Semana.mean(),VE,'{:.1f}',t,'Horas de IA por semana (media)')
fig.suptitle('Uso semanal de IA (horas por día × 7)',x=0.01,ha='left',fontsize=13,fontweight='bold'); fig.tight_layout(); fig.savefig(OUT+'08_uso_semanal.png',bbox_inches='tight'); plt.close()

# 09 scatter horas IA semana vs horas ahorradas
r=df.dropna(subset=['Horas_IA_Semana','Horas_ahorradas_semana'])
fig,ax=plt.subplots(figsize=(7.5,5))
for t,col in [('Estudiante',NA),('Profesional',AZ)]:
    d=r[r.Tipo_Usuario==t]; ax.scatter(d.Horas_IA_Semana,d.Horas_ahorradas_semana,s=22,alpha=.6,color=col,label=t)
m,b0=np.polyfit(r.Horas_IA_Semana,r.Horas_ahorradas_semana,1); xs=np.linspace(r.Horas_IA_Semana.min(),r.Horas_IA_Semana.max(),50)
ax.plot(xs,m*xs+b0,color='k',lw=1.5,label=f'Tendencia: +{m:.2f} h ahorradas por cada hora de IA')
rr=r.Horas_IA_Semana.corr(r.Horas_ahorradas_semana)
ax.set_title(f'Horas de uso de IA vs. horas ahorradas por semana (r = {rr:.2f})',loc='left'); ax.set_xlabel('Horas de IA por semana'); ax.set_ylabel('Horas ahorradas por semana'); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(OUT+'09_uso_vs_ahorro.png',bbox_inches='tight'); plt.close()
print('pendiente',m,'intercepto',b0,'r',rr)

# 10 retorno por herramienta y propósito
fig,ax=plt.subplots(1,2,figsize=(11,3.9))
rt=r.groupby('Herramienta').apply(lambda d:d.Horas_ahorradas_semana.sum()/d.Horas_IA_Semana.sum())
rp=r.groupby('Proposito').apply(lambda d:d.Horas_ahorradas_semana.sum()/d.Horas_IA_Semana.sum())
barh(ax[0],rt,VE,'{:.2f}','Por herramienta','Horas ahorradas por hora de IA')
barh(ax[1],rp,VE,'{:.2f}','Por propósito','Horas ahorradas por hora de IA')
fig.suptitle('Retorno de tiempo: horas ahorradas por cada hora usada',x=0.01,ha='left',fontsize=13,fontweight='bold'); fig.tight_layout(); fig.savefig(OUT+'10_retorno_tiempo.png',bbox_inches='tight'); plt.close()
print(rt.round(3).to_dict()); print(rp.round(3).to_dict())

# 11 heatmap correlaciones
cols={'Horas_IA_Semana':'Horas IA/sem','Horas_ahorradas_semana':'Horas ahorradas/sem','Productividad':'Productividad','Satisfaccion':'Satisfacción','Precision':'Precisión','Costo_mensual_USD':'Costo mensual','Ingreso_mensual':'Ingreso','Edad':'Edad'}
cm=df[list(cols)].rename(columns=cols).corr(); print(cm.round(2).to_string())
fig,ax=plt.subplots(figsize=(7.5,6)); im=ax.imshow(cm,cmap='RdBu_r',vmin=-1,vmax=1)
ax.set_xticks(range(len(cm))); ax.set_xticklabels(cm.columns,rotation=40,ha='right'); ax.set_yticks(range(len(cm))); ax.set_yticklabels(cm.index)
for i in range(len(cm)):
    for j in range(len(cm)): ax.text(j,i,f'{cm.iloc[i,j]:.2f}',ha='center',va='center',fontsize=8,color='white' if abs(cm.iloc[i,j])>.6 else 'black')
ax.set_title('Matriz de correlaciones',loc='left'); fig.colorbar(im,fraction=.04); fig.tight_layout(); fig.savefig(OUT+'11_correlaciones.png',bbox_inches='tight'); plt.close()

# 12 herramienta por tipo (mix)
d=df.dropna(subset=['Herramienta']); ct=pd.crosstab(d.Herramienta,d.Tipo_Usuario); ct=ct.loc[ct.sum(axis=1).sort_values().index]
fig,ax=plt.subplots(figsize=(7.5,4)); ax.barh(ct.index,ct['Estudiante'],color=NA,label='Estudiante'); ax.barh(ct.index,ct['Profesional'],left=ct['Estudiante'],color=AZ,label='Profesional')
ax.set_title('Usuarios por herramienta y tipo',loc='left'); ax.set_xlabel('Usuarios'); ax.legend(frameon=False); fig.tight_layout(); fig.savefig(OUT+'12_herramienta_tipo.png',bbox_inches='tight'); plt.close()

# 13 satisfacción / productividad por herramienta
fig,ax=plt.subplots(1,2,figsize=(11,3.9))
barh(ax[0],d.groupby('Herramienta').Satisfaccion.mean(),AZ,'{:.2f}','Satisfacción media (0-10)','Puntaje'); 
barh(ax[1],d.groupby('Herramienta').Productividad.mean(),NA,'{:.2f}','Productividad media (0-10)','Puntaje')
fig.tight_layout(); fig.savefig(OUT+'13_satisfaccion_productividad.png',bbox_inches='tight'); plt.close()

# tablas para informe
c.dropna(subset=['Herramienta']).groupby('Herramienta').agg(usuarios=('User_ID','count'),gasto_total=('Costo_mensual_USD','sum'),gasto_medio=('Costo_mensual_USD','mean'),pct_paga=('Paga','mean')).sort_values('gasto_total',ascending=False).round(2).to_csv('t_herr.csv')
for by in ['Area','Proposito','Educacion','Tipo_Usuario']:
    c.dropna(subset=[by]).groupby(by).agg(usuarios=('User_ID','count'),gasto_total=('Costo_mensual_USD','sum'),gasto_medio=('Costo_mensual_USD','mean'),pct_paga=('Paga','mean')).sort_values('gasto_total',ascending=False).round(2).to_csv(f't_{by}.csv')
print(pd.read_csv('t_herr.csv').to_string())
for by in ['Area','Proposito','Educacion','Tipo_Usuario']: print(pd.read_csv(f't_{by}.csv').to_string())
