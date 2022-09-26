import numpy as np
import pandas as pd
import random

drug_lsit=["Paracetamol","Ibuprofen","Aspirin","Penicillin","COLOGNE","AUGMENTIN","CEFTRIAXONE",
"CEVAGINE","CEVITIL","CHOLETIMB","CYKLOKAPRON","EPICOCILLIN","ERYTHROCIN","FERRONIL","INSULIN",
"LIGNOPANTHEN","LUCOCID R OINT","MAMILAC WITH IRON","MIGRACID SYRUP","MULTIVIT","NEUROTON","OFLAM",
"OFLOXACIN","OPTICURE","OSSOPAN"]

def rand_msurs(nOfRecs):
    df={}
    df["temperature"]=np.random.choice(np.arange(35.5, 40.5, 0.5), size=nOfRecs)
    df["date"]=list(pd.date_range(start='2018-04-24', end='2018-06-27', periods=nOfRecs))
    df=pd.DataFrame(df)
    df["systolicPressure"]=random.choices(range(110,150),k=nOfRecs)
    df["diastolicPressure"]=random.choices(range(50,86),k=nOfRecs)
    df["condition"]=["High Temperature"]*80+["influenza"]*10+[None]*50+["fine"]*20+[None]*20+["fine"]*20
    df["pulse"]=[75]*20+[None]*50+[75]*130
    df["respration"]=[84]*nOfRecs
    df["sugar"]=random.choices(range(30,400),k=nOfRecs)
    df["oxegen"]=[18]*nOfRecs
    return df



def rand_cmmit(nOfDrugs,nOfRecs):
    alldrugs=[]
    dosage={}

    for drug in random.sample(drug_lsit,k=nOfDrugs):
        dosage[drug]=random.choice(range(1,7))

    df={}
    df["date"]=list(pd.date_range(start='2018-04-24', periods=nOfRecs))
    for day in range(nOfRecs):

        dailydrugs=random.sample(list(dosage.keys()),k=random.choice(range(1,nOfDrugs)))
        alldrugs.append(dailydrugs)
    df["drug"]=alldrugs
    df["Comitment"]=[]
    for day in range(nOfRecs):
        day_comit=[]
        for drug in df["drug"][day]:
            day_comit.append(random.choices(range(0,2),k=dosage[drug]))
        df["Comitment"].append(day_comit)

    df=pd.DataFrame(df)
    return df



def rand_tkn(nOfRecs):
    df={}
    df["completion"]=random.choices(range(1,10),k=nOfRecs)
    df["drug"]=random.sample(drug_lsit, nOfRecs)

    df=pd.DataFrame(df)
    df.completion=df.completion*10
    return df


def rand_TimeLine():
    meddict={"doctor":[],"drug":[],"completion":[]}
    meddict["doctor"]=random.choices(["Ahmed Ali","Mohamed Ali","Khaled Mohamed","Yasser Ahmed","Abdo Yasser"], k=20)
    meddict["completion"]=random.choices(range(1,11),k=20)
    meddict["drug"]=random.sample(drug_lsit, 20)



    df=pd.DataFrame(meddict)
    df.completion=df.completion/10
    df["start_date"]=list(pd.date_range(start='2018-04-24', end='2018-05-27', periods=6))+list(pd.date_range(start='2018-11-22', end='2018-12-27', periods=8))+list(pd.date_range(start='2019-05-23', end='2019-06-7', periods=6))
    df["end_date"]=list(pd.date_range(start='2018-04-30', end='2018-06-07', periods=6))+list(pd.date_range(start='2018-11-30', end='2019-1-07', periods=8))+list(pd.date_range(start='2019-05-30', end='2019-06-16', periods=6))

    return df




#TODO
#nOfRecords
#profile
#list_of_docs
#list_of_conds
#Date,Values()
#Dirstubs
#modeling
#drug_db with common druggg order ---link with probabilty distribution