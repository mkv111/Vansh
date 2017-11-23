# Environment Setup.
from pymongo import MongoClient
from calendar import datetime
import json

client=MongoClient()
db=client['mk']

def AncestryReg():
    global AncestryName, Exist, Selection
    AncestryName=input("\nEnter Your Family/Ancestry/Sir Name:")
    
    cnt=0
    for collnm in db.collection_names():
        if AncestryName in collnm:
            colln=db[collnm]
            creator=colln.find_one({"Relation":"self"},{"Name":1,"_id":0})
            print(str(cnt)+' - '+str(collnm)+' - Created By: '+creator['Name'])
            cnt=cnt+1
            if cnt==0:
                print("There are a few matching ancestry exists in our Database...")
    
    print(str(cnt)+' - Create New')
    MakeSelection()
    selAncestry=Selection
    if selAncestry<=(cnt-1) and selAncestry>=0:
        cnt=0
        for collnm in db.collection_names():
            if AncestryName in collnm:
                if cnt>=selAncestry:
                    AncestryName=collnm
                    Exist=True
                    break
                else:
                    cnt=cnt+1
    elif selAncestry>cnt:
        print("Not an option.. Try again.")
        exit()
    else:
        Exist=False

def ProfileReg():
    global aself, root, markroot, relation, gender, reference, Exist
    name=None;reference=None
    while name=="" or name==None:
        if Exist:
            name=input("\nFull Name of the Member:")
            RefCheck()
            selectGender()
            selectRelation()
        else:
            name=input("\nEnter Your Full Name:")
            selectGender()
            relation="self"

    age=None
    while age=="" or age==None:
        age=input("Enter Age:")

    if markroot=="N":
        root=input("Ancestry Root? (Y/N):")
        if root=="y" or root=="Y":
            markroot="Y";root="Y"
        else:
            root="N";makeroot="N";aself="N"

    if reference==None and aself=="Y":
        reference=relation
    PushData(name, age, relation, root, gender, reference)

    regMore=input("Register more family members? (Y/N)")
    if regMore=="N" or regMore=="n":
        exit()

def PushData(name, age, relation, root, gender, reference):
    global AncestryName, Exist
    if Exist:
        AncestryName=AncestryName
    else:
        AncestryName=(AncestryName+"_"+name+"_"+str(datetime.date.today())).replace(' ','_').replace('-','_')
    coll=db[AncestryName]
    coll.insert({"Name":name, "Age":age, "Gender":gender, "Relation":relation, "Root":root, "Reference":reference})
    Exist=True
    
    # DataFile="../data/"+AncestryName+".csv"
    # Odf=open(DataFile,mode="a")
    # Odf.write("\n"+name+', '+age+', '+root+', '+relation)
    # Odf.close()

def ParamInit():
    global aself, root, markroot, Exist
    aself="Y"
    root="N"
    markroot="N"

def MakeSelection():
    global Selection
    Selection=None
    while not isinstance(Selection,int):
        try:
            Selection=input("Make your selection [0-9]:")
            Selection=int(Selection)
        except BaseException:
            print('Choose one please..')

def RefCheck():
    global AncestryName, Selection, reference
    collnm=db[AncestryName]
    existProfiles=collnm.find({},{"Name":1})
    cnt=0
    for profile in existProfiles:
        print("["+str(cnt)+"]-"+profile['Name'])
        cnt=cnt+1
    print("Find your closest relative in the Ancestry...")
    MakeSelection()
    selReference=Selection
    
    cnt=0; existProfiles=collnm.find({},{"Name":1})
    for profile in existProfiles:
        if cnt==selReference:
            reference=profile['_id']
            break
        else:
            cnt=cnt+1

def selectRelation():
    global relation, reference, AncestryName
    RelationCollnm=db['tree']
    RelationList=RelationCollnm.find({"FIELD2":gender},{"FIELD1":1, "_id":0})
    print("\n")
    cnt=0
    for data in RelationList:
        print("["+str(cnt)+"]-"+data['FIELD1'])
        cnt=cnt+1
    RefName=db[AncestryName].find_one({"_id":reference},{"Name":1})
    print(RefName['Name']+" is Your?")
    MakeSelection()
    selRelation=Selection
    RelationList=RelationCollnm.find({"FIELD2":gender},{"FIELD1":1, "_id":0})
    cnt=0
    for data in RelationList:
        if cnt==selRelation:
            relation=data['FIELD1']
            break
        else:
            cnt=cnt+1

def selectGender():
    global gender
    print("[0]Male\n[1]Female")
    MakeSelection()
    selGender=Selection
    if selGender==0:
        gender="Male"
    else:
        gender="Female"