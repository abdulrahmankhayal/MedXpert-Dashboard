import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
from datetime import datetime as dt
from itertools import compress
import plotly.express as px
from plotly.subplots import make_subplots

import plotly.io as pio
pio.templates[pio.templates.default].layout.colorway=("#660000","#9900FF","#CC0066","#FF9900","#000000","#FF0000")


#Home


symbols={}
symbols[0]="star"
symbols[1]="circle"
symbols[2]="pentagon"
symbols[3]="triangle-up"
symbols[4]="hexagram"




weekdays=[
 'Saturday',
 'Sunday',
 'Monday',
 'Tuesday',
 'Wednesday',
 'Thursday',
 'Friday',
 'Saturday',
 'Sunday',
 'Monday',
 'Tuesday',
 'Wednesday',
 'Thursday',
 'Friday']

colors_scale={0:"gray",1:"blue"}
def getcolor(value):
    return colors_scale[value]

def create_pie(n,row):

    if n== 0 :
        return
    fig=go.Figure()
    fig.add_trace(go.Pie(   
                          values=[row.completion,100-row.completion],
                          hole=0.85,
                          textinfo='none',showlegend=False,hoverinfo="none",
                          marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                          ))
    fig.add_annotation(dict
    (hovertext=row.drug,x=0.5,y=0.5,text=f"{row.completion}%",showarrow=False,font={"size":(30-(0.8*n))}))
    fig.update_layout(title=(row.drug[:20]) if len(row.drug) > 20 else row.drug,title_x=0.5,font=dict(
            #family="Courier New, monospace",
            size=15-(0.3*n),
            color="RebeccaPurple"
        ))
    w=1150/(n)
    if w > 200 :
        w= 200
    fig.update_layout(width=w+10,height=w+10,margin=dict(
        l=1,
        r=1,
        b=1,
        t=35,
        pad=0
    ))
    return fig



def Create_HeatScatt(df,drugs,start,end):

    
    filtered_df=df.copy()

    filtered_df=filtered_df.sort_values("date").set_index("date")[start:end]
    #filtered_df=filtered_df.reset_index()
    filtered_df=filtered_df.tail(28).reset_index()

    if drugs!=[]:
        for idx in range(len(filtered_df.drug)):
            filter_=list(list(filtered_df["drug"].explode().isin(drugs).groupby(level=0))[idx][1])
            filtered_df.at[idx,'drug']=list(compress(filtered_df.drug[idx],filter_))
            filtered_df.at[idx,'Comitment']=list(compress(filtered_df.Comitment[idx],filter_ ))
    filtered_df["total"]=(filtered_df[["Comitment"]].explode(["Comitment"]).groupby(level=0).sum()["Comitment"].apply(np.mean)*100).astype(int)
    
    uniqDrug=filtered_df["drug"].explode().dropna().unique().tolist()
    nofDrugs=len(uniqDrug)
    nofDoses=len(max(filtered_df.Comitment.explode().dropna(), key=len))
    if(len(filtered_df.total))<28:
        
        data=np.pad(filtered_df.total.astype(float), (0, 28 - filtered_df.total.size)
                    ,mode='constant', constant_values=np.nan).reshape(4,7)
        txt=np.pad(filtered_df.date.astype("str"), (0, 28 - filtered_df.date.size), mode='constant', constant_values=np.nan).reshape(4,7)
    else :
        data=np.array(filtered_df.total).reshape(4,7)
        txt=np.array(filtered_df.date.astype("str")).reshape((4,7))
    fig = go.Figure(data=go.Heatmap(colorscale= px.colors.sequential.YlOrRd_r[1:],
                        z=data,zmin=0,zmax=100,
                                   x=[x / 10.0 for x in range((nofDoses+1)*5,(nofDoses+1)*75,(nofDoses+1)*10)],
                                   y=[x / 10.0 for x in range((nofDrugs+1)*5,(nofDrugs+1)*45,(nofDrugs+1)*10)],
                                   text=txt,
                                   hovertemplate= 'Date: %{text}<br>Comitment: %{z}<extra></extra>'
                                   ))
    fig.update_layout(height=800)
    fig.update_yaxes({'anchor': 'x', 'autorange': 'reversed', 'domain': [0.0, 1.0], 'title': {'text': 'Week Number'}})
    fig.update_xaxes({'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'Day of Week'}})

    for dID,drug in enumerate(uniqDrug):
        idx=-1
        shapes=[]
        x=np.array([])
        y=np.array([])
        colors=[]
        for week in range(4):
            for day in range(7):
                idx+=1
                try:
                    dIDX=filtered_df.drug[idx].index(drug)
                except:
                    continue
                shapes+=[symbols[dID]]*len(filtered_df.Comitment[idx][dIDX])
                temp=np.array([i+1 for i in range(len(filtered_df.Comitment[idx][dIDX]))])+((nofDoses+1)*day)
                x=np.append(x,temp)
                temp=np.array([dID+1]*len(filtered_df.Comitment[idx][dIDX]))+((nofDrugs+1)*week)
                y=np.append(y,temp)
                colors+=list(map(getcolor,filtered_df["Comitment"][idx][dIDX]))

        fig.add_trace(go.Scatter(x=x
                             ,y=y,name=drug
                             ,mode="markers",
                  marker={"color":colors,
                         "symbol":shapes,
                         "size":15},hoverinfo="none",
                                    ))
    fig.update_layout(legend=dict(
        orientation="h",

    ))

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    startday=filtered_df.date[0].strftime("%A")
    xlabels=weekdays[weekdays.index(startday):weekdays.index(startday)+7]
    fig.update_xaxes(
        ticktext=xlabels,
        tickvals=[x / 10.0 for x in range((nofDoses+1)*5,(nofDoses+1)*75,(nofDoses+1)*10)]
    )

    fig.update_yaxes(
        ticktext=["Week 1","Week 2","Week 3","Week 4"],
        tickvals=[x / 10.0 for x in range((nofDrugs+1)*5,(nofDrugs+1)*45,(nofDrugs+1)*10)]
    )
    fig.update_layout(
        xaxis={'side': 'top'}, 
    )
    fig.update_layout(legend_title_text='Drug Name:')
    fig.update_layout(height=800)
    #fig.
    #fig.update_layout(margin=dict(l=70, b=50, t=50, r=50))
    #fig.update_layout(width=1200)
    #fig.update_yaxes(automargin=True)

    return fig




#TimeLine
def preprocess(df):
    
    df=df.copy()
    proj_start = df.start_date.min()
    df['start_num'] = (df.start_date-proj_start).dt.days
    df['end_num'] = (df.end_date-proj_start).dt.days
    df['days_start_to_end'] = df.end_num - df.start_num
    df['current_num'] = (df.days_start_to_end * df.completion)
    
    df=df.sort_values(by="start_num")
    deltas=df["start_date"].diff()
    gaps = deltas[deltas > datetime.timedelta(days=30)]
    intervals=[]
    initial=0
    for gap_idx in gaps.index :
        intervals.append([df["start_num"][initial],df["end_num"][gap_idx-1]])
        initial=gap_idx
        if gap_idx == gaps.index[-1] :
            intervals.append([df["start_num"][initial],df["end_num"].max()])
    return df,intervals
def get_fig(df,default=False):
    fig=px.bar(df, x="days_start_to_end", y="drug", color="doctor",base="start_num",barmode="stack",opacity=0.5
               ,hover_data={"start_date":False
                             ,"end_date":False
                             ,"completion":False
                             ,"drug":False
                             ,"days_start_to_end":False
                             ,"start_num":False
                             ,"doctor":False
                           })
    if default==False:
        for plot in fig.data:
            plot["showlegend"]=False
            
    data=px.bar(df, x="current_num", y="drug", color="doctor",base="start_num",barmode="stack"
                ,hover_data={"current_num":False,
                    "start_num":False,"start_date":True,"end_date":True,"completion":True,"drug":True}).data
    for plot in data:
        plot["showlegend"]=False
    fig.add_traces(data)

    return fig


def create_timeline(df,start,end,drugs,doctors):


    filtered_df=df[np.logical_and(df.start_date>=start,df.start_date<=end)]
    if drugs !=[]:
        filtered_df=filtered_df[filtered_df.drug.isin(drugs)]
    if doctors != []:
        filtered_df=filtered_df[filtered_df.doctor.isin(doctors)]
    filtered_df=filtered_df.reset_index()
    filtered_df,intervals=preprocess(filtered_df)
    if len(intervals)>1:
        ratios=[]
        for interval in intervals:
            ratios.append(10+interval[1]-interval[0])
        fig = make_subplots(rows=1, cols=len(intervals), horizontal_spacing = 0.05,shared_yaxes=True,column_widths=ratios,)
    else :
        if len(intervals)==0:
            intervals=[[filtered_df.start_num.min(),filtered_df.end_num.max()]]
        fig = make_subplots(rows=1, cols=1)
        ratios=[]
        for interval in intervals:
            ratios.append(interval[1]-interval[0])

    colors = px.colors.qualitative.Plotly

    #fig.update_layout(title = "Medication TimeLine")

    for subplot in range(1,len(intervals)+1):
        if subplot == 1 :
            fig.add_traces(get_fig(filtered_df,default=True).data)
        else :
            fig.add_traces(get_fig(filtered_df).data,rows=1,cols=subplot)
            fig.update_yaxes(showticklabels=False, row=1, col=subplot)
        upper=intervals[subplot-1][1]+5
        lower=intervals[subplot-1][0]-5
        fig.update_layout({f"xaxis{subplot}" : dict(fixedrange = True,range=[lower,upper])})
        fig.update_layout({f"yaxis{subplot}" : dict(fixedrange = True)})
        visted=[]
        for idx, row in filtered_df[np.logical_and(filtered_df.start_num>=intervals[subplot-1][0],filtered_df.start_num<=intervals[subplot-1][1])].iterrows():
            if row.drug not in visted :
                visted.append(row.drug)
                fig.add_annotation(
            dict(
                xref=f"x{subplot}",
                yref=f"y{subplot}",
                x=row.start_num-4, y=row.drug, # annotation point
                text=f"<b>{row.drug}</b>",

                font=dict(
                size=12
            ),
                showarrow=False,
                width=70,
                hovertext=row.drug,align="left",
            )
        )
            fig.add_annotation(   
            dict(
                xref=f"x{subplot}",yref=f"y{subplot}",
                x=row.end_num+3, y=row.drug, # annotation point
                text=f"<b>{int(row.completion*100)}%</b>",
                showarrow=False,align="right"

            )
        )
    w=sum([10+i[1]-i[0] for i in intervals])*(1+0.05*(len(intervals)-1))*12
    h=50*filtered_df.drug.nunique()
    if w>500:
    
        fig.update_layout(width=w)
    else :
        fig.update_layout(width=500)
    if h>350:
        fig.update_layout(height=h)
    else :
        fig.update_layout(height=350)
    fig.update_xaxes(ticks="outside",ticklen=10,tickwidth=2)
    #fig.update_xaxes(nticks=0)
    fig.update_xaxes(minor_ticks="outside",
                     minor=dict(ticklen=6,tickwidth=1, tickcolor="black"
                                ,tickvals=np.arange(0, filtered_df.end_num.max()+1, 1), showgrid=True))


    fig.update_xaxes(
        ticktext=pd.date_range(filtered_df.start_date.min(), end=filtered_df.end_date.max(),freq="7D").strftime("%d %b %y").tolist(),
        tickvals=np.arange(0, filtered_df.end_num.max()+1, 7),)

    #fig.update_xaxes(mirror="ticks")

    fig.update_layout(barmode='stack')
    fig.update_layout(yaxis=dict(showticklabels=False))
    fig.update_layout(template='plotly_white')
    #fig.update_layout(legend=dict(orientation="h"))
    fig.update_xaxes(showgrid=True, gridwidth=1,gridcolor='LightPink')
    #fig.update_yaxes(showgrid=True, gridwidth=1,)
    fig.update_layout(legend_title_text='Doctor:',legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.05
    ))

    return fig

#Measurements



vitalsrange={
    'pulse':{"min":50,"max":100},
    'respration':{"min":80,"max":100},
    'sugar':{"min":70,"max":200},
    'oxegen':{"min":12,"max":25},

}
vitals=['temperature',
 'pulse',
 'respration',
 'sugar',
 'oxegen',
 'systolicPressure',
 'diastolicPressure']


def set_hshapes(fig,df,vital,row,col):
    #fig.update_yaxes(tick0=0, dtick=2)
    if(df[vital].min()<vitalsrange[vital]["min"]+5):

        fig.add_hline(y=vitalsrange[vital]["min"], line_dash="dash", line_color="red",row=row,col=col,
                  annotation=dict(text="Lower Crtical",xref="paper",yref="paper",x=1.05, showarrow=False))
        fig.add_hrect(y1=vitalsrange[vital]["min"],y0=df[vital].min()-5,fillcolor="red",
                      opacity=0.4,layer="below", line_width=0,row=row,col=col)
    if(df[vital].max()>vitalsrange[vital]["max"]-5):
        if vital != "respration":
            fig.add_hline(y=vitalsrange[vital]["max"], line_dash="dash", line_color="red",row=row,col=col,
                      annotation=dict(text="Upper Crtical",xref="paper",yref="paper",x=1.05, showarrow=False))
            fig.add_hrect(y0=vitalsrange[vital]["max"],y1=df[vital].max()+5,fillcolor="red",
                          opacity=0.4,layer="below", line_width=0,row=row,col=col)

def create_lines(df,user_vitals,start,end,style,conds):
    filtered_df=df.sort_values("date").set_index("date")[start:end]
    nofvitals=len(user_vitals)
    if user_vitals!=[]:
        if "Pressure" in user_vitals:
            user_vitals.remove("Pressure")
            user_vitals=user_vitals+['systolicPressure']+['diastolicPressure']
        filtered_df=filtered_df[[*user_vitals,"condition"]]

    else:
        user_vitals=['temperature', 'pulse', 'respration', 'sugar', 'oxegen', 'systolicPressure', 'diastolicPressure']
        nofvitals=6
    if conds!=[]:
        filtered_df=filtered_df[filtered_df.condition.isin(conds)]
    height=250*nofvitals
    fig=make_subplots(rows=nofvitals, cols=1,
        subplot_titles=(user_vitals[:-2]+["Pressure"]) if "systolicPressure" in user_vitals else user_vitals)
    for sbplt_tit in range (nofvitals):
        fig.layout.annotations[sbplt_tit].update(y=fig.layout.annotations[sbplt_tit]["y"]+0.02+0.005*(6-nofvitals))
    fig.update_layout(
        height=250*nofvitals)
    nofvitals=len(user_vitals)
    for id,vital in enumerate(user_vitals):
        if vital == "diastolicPressure":
            id-=1
        fig.add_trace(go.Scatter(x=filtered_df.index,y=filtered_df[vital],name=vital,legendgroup=id,customdata=filtered_df["condition"],
                                hovertemplate='Date: %{x}<br>Value: %{y}<br>Condition: %{customdata}<extra></extra>',mode='lines')
                      ,row=id+1,col=1)
    if "systolicPressure" in user_vitals:
        fig.update_layout(legend_tracegroupgap =height/(nofvitals))

        
    #fig.update_layout(hovermode="x unified")
    
    else : 
        fig.update_layout(legend_tracegroupgap =height/(nofvitals+1),    )
    
    if "Show Conditon" in style:

        conditions=filtered_df.condition.unique()
        conditions= [i for i in filtered_df.condition.unique() if i ]
        colordic={}
        colors=["red", "green", "blue", "goldenrod", "magenta"]

        for idx,cond in enumerate(conditions):
            colordic[cond]=colors[idx]
        id=0

        for _, v in filtered_df.groupby((filtered_df['condition'].shift() != filtered_df['condition']).cumsum()):

            if v.condition.unique()[0]:
                fig.add_vrect(x0=v.index.min(),
                          x1=v.index.max(), opacity=0.3,layer="below", line_width=0,fillcolor=colordic[v.condition.unique()[0]],
                          annotation={"x":v.index.min()+(v.index.max()-v.index.min())*0.7,"align":"center","y":1.15,"text":v.condition.unique()[0],"showarrow":False},)
                id+=1
    if "Show guidelines" in style:
        for idx,vital in enumerate(user_vitals):

            if vital == "temperature":
                fig.add_hline(y=37.7, line_dash="dash", line_color="red",row=idx+1,col=1,
                  annotation=dict(text="Crtical",xref="paper",yref="paper",x=1.05, showarrow=False))
                fig.add_hrect(y0=37.7,y1=38.3,fillcolor="red", opacity=0.1,layer="below", line_width=0,row=idx+1,col=1)
                fig.add_hrect(y0=38.3,y1=39.3,fillcolor="red", opacity=0.25,layer="below", line_width=0,row=idx+1,col=1)
                fig.add_hrect(y0=39.3,y1=40,fillcolor="red", opacity=0.40,layer="below", line_width=0,row=idx+1,col=1)
                fig.add_hrect(y0=40,y1=df.temperature.max(),fillcolor="red", opacity=0.55,layer="below", line_width=0,row=idx+1,col=1)
            else:
                if vital in ['systolicPressure','diastolicPressure']:
                    continue
                set_hshapes(fig,filtered_df,vital,idx+1,1)
    return fig

