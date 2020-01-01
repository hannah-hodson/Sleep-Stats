# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 08:18:59 2018

@author: Hannah
"""
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator



df = pd.read_csv(r"C:\Users\Hannah\AnacondaProjects\Sleep Stats\Sleep stats.csv")

df["st_Date"] = ""
df["st_Bedtime"] = ""
df["st_SO"] = ""
df["st_Awake"] = ""
df["td_TST"] = ""
df["st_TST"] = ""
df["td_WASO"] = ""
df["st_WASO"] = ""
df["h_TST"] = "" 
df["h_WASO"] = "" 
df["st_SC"] = ""
df["td_HBM"] = ""
df["h_HBM"] = ""
df["td_HAM"] = ""
df["h_HAM"] = ""
df['Meditation'] = ""
df["Sleep Meditation"] = df["Sleep Meditation"].astype(str)
df["Mindfulness Meditation"] = df["Mindfulness Meditation"].astype(str)
df["td_SOL"] = ""
df["td_SB"] = ""
df["h_SB"] = ""




for i, row in df.iterrows():
    
    #print "row no.", i, ": "
    
    #make strptimes
    df["st_Date"].iloc[i] = dt.strptime(df["Date"].iloc[i], "%d.%m.%y")
    df["st_SC"].iloc[i] = dt.strptime(df["Date"].iloc[i] + " " + df["Screen curfew"].iloc[i], '%d.%m.%y %H:%M') 
    df["st_SO"].iloc[i] = dt.strptime(df["Date"].iloc[i] + " " + df["SO"].iloc[i], '%d.%m.%y %H:%M') 
    df["st_Awake"].iloc[i] = dt.strptime(df["Awake"].iloc[i], '%H:%M') 
    df["st_Bedtime"].iloc[i] = dt.strptime(df["Date"].iloc[i] + " " + df["Bedtime"].iloc[i], '%d.%m.%y %H:%M') 
    
    

    #calculate HBM & HAM as td
    hours_before_midnight = timedelta()
    hours_after_midnight = timedelta()   
    if(df["st_SO"].iloc[i] > dt.strptime("12:00", '%H:%M')):
        hours_before_midnight = dt.strptime("23:59", '%H:%M')  - df["st_SO"].iloc[i] + timedelta(minutes=1)
        hours_after_midnight = df["st_Awake"].iloc[i] - dt.strptime("00:00", '%H:%M')
    else:
        hours_after_midnight = df["st_Awake"].iloc[i] - df["st_SO"].iloc[i]      
    df["td_HBM"].iloc[i] = hours_before_midnight  
    df["td_HAM"].iloc[i] = hours_after_midnight
    

    
    #calculate hours (float)
    df["h_HBM"].iloc[i] = float(df["td_HBM"].iloc[i].seconds)/3600
    df["h_HAM"].iloc[i] = float(df["td_HAM"].iloc[i].seconds)/3600                
    df["h_WASO"].iloc[i] = float(df["WASO"].iloc[i][:1]) + float(df["WASO"].iloc[i][3:])/60  
    df["h_TST"].iloc[i] = float(df["h_HBM"].iloc[i] + df["h_HAM"].iloc[i] - df["h_WASO"].iloc[i])
                                          
    #make Meditation col 
    if(df["Sleep Meditation"].iloc[i]=='0' and df["Mindfulness Meditation"].iloc[i]=='0'):
        df['Meditation'].iloc[i] = 0
    else:
        df['Meditation'].iloc[i] = 1



    #calculate SOL
    df["td_SOL"].iloc[i] = df["st_SO"].iloc[i] - df["st_Bedtime"].iloc[i]
    
    #calculate bedtime-SC
    df["td_SB"].iloc[i] = df["st_Bedtime"].iloc[i] - df["st_SC"].iloc[i]
    df["h_SB"].iloc[i] = float(df["td_SB"].iloc[i].seconds)/3600




def line_vsdate(ycol):
    
    fig, ax = plt.subplots(1,1) 
    ax.plot(df["Date"], df["h_"+ycol])
    ax.set_title(ycol)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.xticks(rotation=90)
    #ax.yaxis.set_major_locator(mdates.HourLocator())
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    #ax.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel('date')
    ax.set_ylabel(ycol + ' /hours')
    
    print "avg " + ycol + " = " + str(float(sum(df["h_"+ycol])) / len(df["h_"+ycol])) + " hours"




def sp_box(ax, xcol, ycol, title, ylabel):
    ax.boxplot([list(df[df[xcol]==0][ycol]), list(df[df[xcol]!=0][ycol])])
    ax.set_title(title)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(['no ' + xcol + "\nn=" + str(len(list(df[df[xcol]==0][ycol]))), xcol + "\nn=" + str(len(list(df[df[xcol]!=0][ycol])))])


def box_sleepvsvar(xcol): 
    fig, ax = plt.subplots(2,2)
    sp_box(ax[0][0], xcol, "h_TST", 'Hours of Sleep', 'TST /hours')
    sp_box(ax[0][1], xcol, "h_HBM", 'Hours before Midnight', "HBM")
    sp_box(ax[1][0], xcol, "h_WASO", 'Wake after sleep onset', 'WASO /hours')
    sp_box(ax[1][1], xcol, "Quality /10", 'Sleep Quality', 'sleep quality /10')
    plt.tight_layout()


def sp_scatter(ax, df, xcol, ycol, title, xlabel, ylabel):
    df.set_index(xcol, drop=False, inplace=True)
    df[ycol].plot(ax=ax, style=".")
    #df.plot(x=xcol, y=ycol, style=".", ax=ax)  
    ax.set_title(title)
    ax.set_xlim(df[xcol].min(), df[xcol].max())
    ax.set_ylim(df[ycol].min(), df[ycol].max())
    #ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel(ylabel)
    #ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel(xlabel)
    #ax.legend_.remove()
    

def scatter_sleepvstime(df, xcol, xlabel, title):  
         
    fig, ax = plt.subplots(2,2)
    sp_scatter(ax[0][0], df, xcol, "h_TST", "Hours of Sleep", xlabel, 'TST /hours')
    sp_scatter(ax[0][1], df, xcol, "h_HBM", "Hours before Midnight", xlabel, 'HBM')    
    sp_scatter(ax[1][0], df, xcol, "h_WASO", "Wake After Sleep Onset", xlabel, 'WASO/ hours') 
    sp_scatter(ax[1][1], df, xcol, "Quality /10", "Sleep Quality", xlabel, 'Quality /10')
    plt.tight_layout()




scatter_sleepvstime(df, "h_SB", 'Screen Break /hours', 'Screen Break')




    


#box_sleepvsvar("Meditation")
#line_vsdate("WASO")














''' Sleep quality vs TST - swap axes
ax[1].boxplot([ list(df[df["Quality /10"]==i]["h_TST"])  for i in range(0,11)])
ax[1].set_title('Hours of Sleep')
ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
#plt.xticks([1,2], ['no pain', 'pain'])
ax[1].set_ylabel('TST /hours')
ax[1].set_xlabel('sleep quality')
'''


'''
def timecon(col):
    # td = timedelta object (time gap)
    # st = strptime object (single point in time)
    # h = hours (float)
    df["td_"+col] = ""
    df["st_"+col] = ""
    df["h_"+col] = ""
    
    for i, row in df.iterrows():     
        try:            
            df["td_"+col].iloc[i] =                                                                              
            df["st_"+col].iloc[i] = dt.strptime("00:00", '%H:%M') + df["td_"+col].iloc[i]            
            df["h_"+col].iloc[i] = float(df["td_"+col].iloc[i].seconds)/3600
            
        except:
            print "exception in timecon"    
'''

'''
def strptime(col):
    df["st_"+col] = ""
    for i, row in df.iterrows(): 
     
        try:                                                                                                 
            df["st_"+col].iloc[i] = dt.strptime(df[col].iloc[i][:2]) + ":" + float(df[col].iloc[i][3:], '%H:%M')              
        except:
            print "exception in strptime"
'''

