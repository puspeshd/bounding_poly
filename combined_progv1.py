
import cv2
from google.cloud import vision
import os
import re
import logging
from flask import Flask,request,render_template
from fileinput import filename
import requests
from flask_cors import CORS,cross_origin
import json
import gzip
import pandas as pd
import math
import numpy
from scipy import ndimage
import fitz
import datetime
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'chetan.json'
client = vision.ImageAnnotatorClient()

def rotate_image(word_list_sorted,image_path):
    img=cv2.imread(image_path)
    for i in range(10):  
        print(word_list_sorted[i][0][0][0],type(word_list_sorted[i][0][0]))
    v1=(1,2)
    v2=(2,2)
    for i in range(len(word_list_sorted)):
        if(word_list_sorted[i][1]["t_"].lower().find("income")>-1 or word_list_sorted[i][1]["t_"].lower().find("unique")>-1):
            print(word_list_sorted[i][1]["t_"])
            v1=word_list_sorted[i][0][0]
            for j in range(0,len(word_list_sorted)):
                if(word_list_sorted[j][1]["t_"].lower().find("department")>-1 or word_list_sorted[j][1]["t_"].lower().find("identification")>-1):
                    v2=word_list_sorted[j][0][0]
                    print(word_list_sorted[j][1]["t_"])
                    break      
            break
    x1,x2,y1,y2= v1[0],v2[0],v1[1],v2[1]
    base=abs(x1-x2)
    perp=abs(y1-y2)
    print(base,perp)
    print(x1,y1,x2,y2)
    if(base==0):
        theta=90
    else:
       theta=perp/base        
    if(perp>0):
       pass
    else:     
        print(theta)
        xo=numpy.arctan(theta)
        xo=numpy.rad2deg(xo)
        if(y1>y2 and x1==x2):
            img=ndimage.rotate(img,-xo,reshape=True)
            print("CASE 0")
        elif(y2>y1 and x1==x2):    
            img=ndimage.rotate(img,xo,reshape=True)
            print("CASE 1")
        elif(y1>y2 and x2>x1):    
            img=ndimage.rotate(img,-xo,reshape=True)
            print("CASE 2")
        elif(y2>y1 and x1>x2):    
            img=ndimage.rotate(img,(180-xo),reshape=True)
            print("CASE 3")
        elif(y1>y2 and x1>x2):    
            img=ndimage.rotate(img,-(180-xo),reshape=True)
            print("CASE 4")
        elif(y2>y1 and x2>x1):
            img=ndimage.rotate(img,xo,reshape=True)
            print("CASE 5")                
        
        print(xo, "this will be rotation angle .... SHOUT OUT A BIG CONGRATS TO YOURSELF MAN")
    cv2.imwrite(image_path,img)    
    return image_path




def retsortedwords(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Creates an image object
    image = vision.Image(content=content)

    # Performs OCR on the image
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    '''desc = annotations[0].description
    #print(desc.encode("utf-8"))'''


    word_bounding_vertices = []

    # Extracts word bounding vertices
    for annotation in annotations[1:]:
        annotation1 = annotation.description
        annotation1 = str(annotation1).encode('utf-8')
        annotation1 = str(annotation1)
        annotation1 = annotation1.replace("\\", "")
        annotation1 = annotation1.replace("|", "")
        annotation1 = annotation1.replace("/", " ")
        annotation1 = annotation1.replace("'\*", " ")
        annotation1 = annotation1.replace("'", "")
        annotation1 = annotation1.replace("\n", " ")
        annotation1 = re.sub("x..", "", annotation1)
        annotation1 = annotation1.replace("(", "")
        annotation1 = annotation1.replace(")", "")
        annotation1 = list(annotation1)
        annotation1 = annotation1[1:]
        annotation1 = "".join(annotation1)
        #print(annotation1,end="*") 
        if(annotation1.replace(' ','').isalpha()):
           type="ALPHA"
        elif(annotation1.replace(' ','').isdigit()):
            type="DIGIT"
        elif(annotation1.replace(' ','').isalnum()):
            type="ALPHANUMERIC" 
        elif(len(annotation1.replace(' ',''))<1):
            type="NULL"
        else:
            type="SPECIAL CHARACTER/S"           
        vertices = [(vertex.x, vertex.y)for vertex in annotation.bounding_poly.vertices]
        

        word_bounding_vertices.append([vertices,{"t_": annotation1},{"length":len(annotation1),"type":type}])
    #word_bounding_vertices = sorted(word_bounding_vertices, key= lambda x: x[0][0][1])
    length=len(word_bounding_vertices)-1
    while length>-1:
        ##print(word_bounding_vertices[length])
        if(word_bounding_vertices[length][1]['t_']==''):
            word_bounding_vertices.pop(length)
        length=length-1
    #print(len(word_bounding_vertices)," THIS IS LENGTH AFTER TRIMMING")
    return word_bounding_vertices  
def retsortedwords2(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Creates an image object
    image = vision.Image(content=content)

    # Performs OCR on the image
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    '''desc = annotations[0].description
    #print(desc.encode("utf-8"))'''


    word_bounding_vertices = []

    # Extracts word bounding vertices
    for annotation in annotations[1:]:
        annotation1 = annotation.description
        annotation1 = str(annotation1).encode('utf-8')
        annotation1 = str(annotation1)
        annotation1 = annotation1.replace("\\", "")
        annotation1 = annotation1.replace("|", "")
        annotation1 = annotation1.replace("/", " ")
        annotation1 = annotation1.replace("'\*", " ")
        annotation1 = annotation1.replace("'", "")
        annotation1 = annotation1.replace("\n", " ")
        annotation1 = re.sub("x..", "", annotation1)
        annotation1 = annotation1.replace("(", "")
        annotation1 = annotation1.replace(")", "")
        annotation1 = list(annotation1)
        annotation1 = annotation1[1:]
        annotation1 = "".join(annotation1)
        #print(annotation1,end="*") 
        if(annotation1.replace(' ','').isalpha()):
           type="ALPHA"
        elif(annotation1.replace(' ','').isdigit()):
            type="DIGIT"
        elif(annotation1.replace(' ','').isalnum()):
            type="ALPHANUMERIC" 
        elif(len(annotation1.replace(' ',''))<1):
            type="NULL"
        else:
            type="SPECIAL CHARACTER/S"           
        vertices = [(vertex.x, vertex.y)for vertex in annotation.bounding_poly.vertices]
        

        word_bounding_vertices.append([vertices,{"t_": annotation1},{"length":len(annotation1),"type":type}])
    word_bounding_vertices = sorted(word_bounding_vertices, key= lambda x: x[0][0][1])
    length=len(word_bounding_vertices)-1
    while length>-1:
        ##print(word_bounding_vertices[length])
        if(word_bounding_vertices[length][1]['t_']==''):
            word_bounding_vertices.pop(length)
        length=length-1
    #print(len(word_bounding_vertices)," THIS IS LENGTH AFTER TRIMMING")
    return word_bounding_vertices  
def columnar_new(image_path,word_bounding_vertices) :
    xo=0
    while xo<len(word_bounding_vertices):
        if(len(word_bounding_vertices[xo][1]["t_"])<1):
            word_bounding_vertices.pop(xo)
        xo+=1
    column_list=[]
    for i in range(len(word_bounding_vertices)):
        column_name=[]
        for j in range(i,len(word_bounding_vertices)):
         if(abs(word_bounding_vertices[i][0][0][0]-word_bounding_vertices[j][0][0][0])<=50):
          #if(str(column_list).find(str(column_name))==-1):   
             column_name.append(word_bounding_vertices[j])
        
        column_list.append(column_name)
    
    
    fin_list=[]
    temp_list=[]
    x=1
    img=cv2.imread(image_path)
    h,w,_=img.shape
    ##print(h,w)
    #exit()
    for i in column_list:
        new_list=[]
        if(i[0][0][0][0]<w//3):
                new_list.append(f"LC{x}->")
        elif(i[0][0][0][0]>w//3+w//3):
                new_list.append(f"RC{x}->")
        else:
                new_list.append(f"CC{x}->")      
        for j in range(len(i)):
            if(i[j][1]["t_"] not in temp_list):
                new_list.append(i[j][1]["t_"])
                temp_list.append(i[j][1]["t_"])
        x+=1
        fin_list.append(new_list)
       
     
    
    fina_list=[]
    for i in fin_list:
        if(len(i)>1):
            fina_list.append(i)
    left_columns=[]
    right_columns=[]
    center_columns=[]
    for i in fina_list:
        if(bool(re.search("LC\d->",i[0]))==True or bool(re.search("LC\d\d->",i[0]))==True):
            left_columns.append(i)
        elif(bool(re.search("CC\d->",i[0]))==True or bool(re.search("CC\d\d->",i[0]))==True):
            center_columns.append(i)    
        elif(bool(re.search("RC\d->",i[0]))==True or re.search("RC\d\d->",i[0])==True):
            right_columns.append(i)
    x=open("file1.txt","w+")
    x.write("\n_________________________________________LEFT COLUMNS___________________________________________\n\n")        
    #print("____________________________________LEFT COLUMNS__________________________________\n\n")
    for i in range(len(left_columns)):
        left_columns[i][0]=re.sub("LC\d->",f"LC{i}->",left_columns[i][0])
        left_columns[i][0]=re.sub("LC\d\d->",f"LC{i}->",left_columns[i][0])
        #print(left_columns[i])
        x.write(str(left_columns[i])+"\n")
    x.write("\n_________________________________________RIGHT COLUMNS___________________________________________\n\n")
    #print("____________________________________RIGHT COLUMNS__________________________________\n\n")
    for i in range(len(right_columns)):
        right_columns[i][0]=re.sub("RC\d->",f"RC{i}->",right_columns[i][0])
        right_columns[i][0]=re.sub("RC\d\d->",f"RC{i}->",right_columns[i][0])
        #print(right_columns[i])
        x.write(str(right_columns[i])+"\n") 
    x.write("\n_________________________________________CENTER COLUMNS___________________________________________\n\n")
    #print("____________________________________CENTER COLUMNS__________________________________\n\n")
    for i in range(len(center_columns)):
        center_columns[i][0]=re.sub("CC\d->",f"CC{i}->",center_columns[i][0])
        center_columns[i][0]=re.sub("CC\d\d->",f"CC{i}->",center_columns[i][0])
        #print(center_columns[i])    
        x.write(str(center_columns[i])+"\n")
    x.close()
    return fina_list
def linemaker(word_list_sorted):
    i = 0
    listfin = []

    while i < len(word_list_sorted):
        x = word_list_sorted[i][0][0][1]
        list1 = []
        #list1.append(word_list_sorted[i]) 
        for j in range(i, len(word_list_sorted)):
            if abs(word_list_sorted[j][0][0][1]-x)<=5 :
                list1.append(word_list_sorted[j])
                
            else:
                break
            
            i = j+1
        listfin.append(list1)
    for i in range(len(listfin)):
        listfin[i]=sorted(listfin[i],key=lambda x: x[0][0][0])
        #print(listfin[i])  
    
    ##print(listfin[1],"jhgfhgfhg")    
    dict_to_insert_later={"demo":"BLUEALGO"}    
    for iii in range(len(listfin)):
        new_line=[]
        for i in range(len(listfin[iii])-1):
            if(abs(listfin[iii][i][0][1][0]-listfin[iii][i+1][0][0][0])>50):
               ##print(listfin[iii][i][0][1][0],listfin[iii][i+1][0][0][0])
               new_line=listfin[iii][i+1:]
               listfin[iii]=listfin[iii][0:i+1]
               dict_to_insert_later.update({iii+1:new_line})
               break
    ##print(len(listfin),"THIS IS LENGTH BEFORE ADDING ELEMENTS")
    del dict_to_insert_later["demo"]
    for i in dict_to_insert_later:
        
        #print(i,dict_to_insert_later[i],"SEE ME ")
        listfin.insert(i,dict_to_insert_later[i])
        ##print(dict_to_insert_later[i],listfin[i],"COMPARING HERE ")          
    ##print(len(listfin),"THIS IS LENGTH AFTER ADDING ELEMENTS")
     
    return(listfin)    
def columnmaker(listfin):
    
    columnlist={}
    no=1
    length=len(listfin)
    checklist=[]
    x=0
    while x<length:
        collist=[]
        for j in range(x,length):
            ##print(x,"THIS IS J s value in  x")
            ##print(abs(listfin[x][0][0][0][0]-listfin[j][0][0][0][0]))
            if(abs(listfin[x][0][0][0][0]-listfin[j][0][0][0][0])<30 and listfin[j] not in checklist):
                 collist.append(listfin[j])
                 checklist.append(listfin[j])
                 
                 
        x=x+1         
        if(len(collist)>0):    
            columnlist.update({no:collist})
            no+=1

  
    ##print(columnlist,"HERE")
    ##print("SADASDASDJHDFHJSFGDJKHFGJKDFHSKFHDSKHFK")
    
    x=open("file1.txt","w+")
    x.write("TOTAL COLUMNS ->"+str(len(columnlist.keys()))+"\n")
    lolalist=[]
    #print(columnlist.keys())
    for i in  columnlist.keys():
        
        ##print(len(columnlist[i]))
        stringer=''
        for j in range(len(columnlist[i])):
         
         for k in range(len(columnlist[i][j])): 
         ##print(j,"SEE ME SOON \n")
         #x.write(str(i)+"->"+str(columnlist[i][0][0][1]["t_"])+" -> "+" NO OF WORDS IN THIS column -> "+str(len(columnlist[i]))+"\n")    
         ##print(columnlist[i][0][j][1]["t_"])
          
      
           stringer=stringer+" "+columnlist[i][j][k][1]["t_"]
        
        lolalist.append(stringer)  
        #x.write("COLUMN----------------------------------------\n"+stringer+"\n\n\n") 
    for i in range(len(lolalist)):
        
        x.write("COLUMN--------------------------------\n\n"+lolalist[i]+"\n--------------------------------\n")    
    x.close()
    for i in columnlist:
        ##print(columnlist[i])
        pass
def lineswithcol(image_path,listfin):
    img=cv2.imread(image_path)
    h,w,_=img.shape
    
    i=0
    j=0
    lc_col=0
    rc_col=0
    cc_col=0
    while i<len(listfin):
        
        flag=''
        for x in listfin[i]:
            key=x[0][0][0]
            if(key<w//3):
                key_col=lc_col+1
                flag='left'
            elif(key>w//3+w//3):
                key_col=rc_col+1
                flag='right'
            else:
                key_col=cc_col+1
                flag='center'
            for k in range(len(listfin)):
                l=0
                while l<len(listfin[k]):
                 if(abs(listfin[k][l][0][0][0]-key)<150):
                    if(len(listfin[k][l])==3): 
                        listfin[k][l].append(f" {flag}_C {key_col}  ")
                 l+=1
            if(flag=='left'):
                lc_col+=1
            elif(flag=='right'):
                rc_col+=1  
            elif(flag=='center'):
                cc_col+=1           
        i+=1  
    i=0
    j=0
    lc_col=0
    rc_col=0
    cc_col=0
    while i<len(listfin):
        
        flag=''
        for x in listfin[i]:
            key_l=x[0][0][0]
            key_r=x[0][1][0]
            key_c=(key_l+key_r)//2
            fola=0
            for k in range(len(listfin)):
                l=0
                while l<len(listfin[k]):
                 if(abs(listfin[k][l][0][0][0]-key_l)<10):
                    if(len(listfin[k][l])<=4): 
                        flag="LA"
                        listfin[k][l].append(f" {flag} {lc_col}  ")
                        listfin[k][l].insert(5,fola)
                        fola+=1
                 elif(abs(listfin[k][l][0][1][0]-key_r)<10):
                    if(len(listfin[k][l])<=4): 
                        flag="RA"
                        listfin[k][l].append(f" {flag} {rc_col}  ")
                        listfin[k][l].insert(5,fola)
                        fola+=1
                 elif(abs((listfin[k][l][0][0][0]+listfin[k][l][0][1][0])//2-key)<10):
                    if(len(listfin[k][l])<=4): 
                        flag="CA"
                        listfin[k][l].append(f" {flag} {cc_col}  ")              
                        listfin[k][l].insert(5,fola)
                        fola+=1
                 l+=1
            if(flag=='LA'):
                lc_col+=1
            elif(flag=='RA'):
                rc_col+=1  
            elif(flag=='CA'):
                cc_col+=1           
        i+=1
    for i in range(len(listfin)):
        for j in range(len(listfin[i])):
            valu=listfin[i][j][len(listfin[i][j])-2]
            ##print(valu)
            if(len(re.findall(valu,str(listfin))))<2:
                       listfin[i][j][len(listfin[i][j])-2]=000
                                



         
    return listfin                 
def maketemplate(image_path,list_fin):
   uriidentifier=[]
   for i in range(len(list_fin)):
       stro=''
       for j in range(len(list_fin[i])):
           #print(list_fin[i][j][1]["t_"],end=" ")
           stro=stro+list_fin[i][j][1]["t_"]+" "
       uriidentifier.append(stro)
       #print("\n")
   f=open("uri_final.txt","r+")
   x=f.read()
   
   x=x.split(",")
   for i in range(len(uriidentifier)):
       for word in x:
           
           if(uriidentifier[i].lower().replace("\"","").find(word.lower())>-1):
               #print("FOUND")
               list_fin[i].insert(0,{"uri":"ba_"+word.replace(" ","_")})
   #x=open(image_path.replace(".jpg",".txt").replace(".\w\w\w",".txt").replace(".\w\w\w\w",".txt"),"w+")
   image_path=image_path.split(".")
   image_path[1]="txt"
   image_path=".".join(image_path)
   #print(image_path,"THIS IS TEST")
   x=open(image_path,"w+")
   for i in range(len(list_fin)):
       if(type(list_fin[i][0])==dict): 
         if(type(list_fin[i][1])==dict and list_fin[i][1]["uri"]=="ba_fathers_name"):  
           #print(list_fin[i][1],end=" ")
           x.write(str(list_fin[i][1])+" ") 
           list_temp=list_fin[i][2:]
         else:
             #print(list_fin[i][0],end=" ")
             x.write(str(list_fin[i][0])+" ") 
             list_temp=list_fin[i][1:] 
       else:
           list_temp=list_fin[i]  
       if(type(list_temp[0])==dict):
           #print(list_temp[0],end=" ")
           x.write(str(list_temp[0])+" ")
           list_temp=list_temp[1:]      
       for j in range(len(list_temp)):
           
           if(list_temp[j][2]["type"]=="ALPHANUMERIC" and len(list_temp[j][1]["t_"])==10 and bool(re.search("\w\w\w\w\w\d\d\d\d\w",list_temp[j][1]["t_"]))==True):
               #print({"uri":"ba_pan_no"},end=" ")
               x.write(str({"uri":"ba_pan_no"})+" ")
           try:    
            if(list_temp[j][2]["type"]=="DIGIT" and list_temp[j+1][2]["type"]=="DIGIT" and list_temp[j+2][2]["type"]=="DIGIT" and len(list_temp)-1==j+2):
               x.write(str({"uri":"aadhar_no"})+" ")
               #print("AADHAR NO IS ::::: ",list_temp[j][1]["t_"],list_temp[j+1][1]["t_"],list_temp[j+2][1]["t_"])
           except:
               pass         
           #print(list_temp[j][2]["type"],"length=",len(list_temp[j][1]["t_"]),end=" ")
           #x.write(list_temp[j][2]["type"]+" length="+str(len(list_temp[j][1]["t_"]))+" ")    
           x.write(list_temp[j][2]["type"]+" ")          
       #print("\r")
       x.write("\n")           
   x.close() 
   return [uriidentifier,list_fin]        
def elasticcode(image_path):
    ### elastic search code starts here only for jpg files right now 
    #with open(image_path.replace(".jpg",".txt") ,"r") as f: #this is only for jpg right now
    image_path=image_path.split(".")
    image_path[1]="txt"
    image_path=".".join(image_path)
    print(image_path,"THIS IS TEST")
    with open(image_path,"r") as f:
        content = f.read()
        content=content.replace("\n","").replace("{","").replace("}","").replace(":","").replace("/","")
        ##print(content)
    # Prepare the search query
    query = {
        
        "query": {
            "query_string":{
             
                
                "query": content,
                "fuzziness":"0",
                
                
                
            
            }
        }
       
    
    }
    # Convert the query to JSON and gzip compress it
    query_data = json.dumps(query).encode('utf-8')
    compressed_query = gzip.compress(query_data)

    # Set up the Elasticsearch endpoint and authentication
    url = "https://elastic.bluealgo.com/bankdata/_search"
    auth = ("elastic", "2dcTr656H0mUt6iHY2K1w14M")

    # Set the headers for the request
    headers = {"Content-Type": "application/json" ,"Content-Encoding":"gzip"}

    # Send the GET request with the query
    response = requests.get(url, data=compressed_query, auth=auth, headers=headers)

    # Process the response as needed
    ##print(response.json())

    # Get the search results
    results = response.text
    
        
    #print(results,"HAH A ")
    #print(results)
    results=results[results.find("\"id:")+4:results.find("_template")+9]


    #print(results)
    return results      

                   
def aadhar_front4_template(text_list_0):
   
    #print(text_list)
    name=''
    dob=''
    gender=''
    aadhar_no=''
    gen_ind=0

    for i in range(len(text_list_0)):
        
               
        if(text_list_0[i].lower().find("date of birth")>-1 or text_list_0[i].lower().find("year of birth")>-1 or text_list_0[i].lower().find(" dob ") >-1 or text_list_0[i].find('DOB')>-1):
            dob=text_list_0[i]
            date_index=i            #date to be extracted later specifically   
        if(bool(re.search("\WMALE",text_list_0[i]))==True or bool(re.search("\WMale",text_list_0[i]))==True):
            gender="MALE"
            gen_ind=i
        elif(bool(re.search("FEMALE",text_list_0[i]))==True or bool(re.search("Female",text_list_0[i]))==True):
            gender="FEMALE"
            gen_ind=i    
        if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",text_list_0[i]))==True):
            aadhar_no=text_list_0[i]
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")        
    try:
        name=text_list_0[date_index-1]
        if(name.find("MALE")>-1 or name.find("Male")>-1 or name.find("Female")>-1):
            name=text_list_0[date_index-2]
    except:
        if(gen_ind>0):
            dob=text_list_0[gen_ind-1]
            name=text_list_0[gen_ind-2]        
        else:
            pass        
    fin_res={"Name":name,"DOB":dob,"GENDER":gender,"Aadhar_no":aadhar_no}

    return(fin_res)        
def aadhar_front3_template(text_list_0):
   
    #print(text_list)
    name=''
    dob=''
    gender=''
    aadhar_no=''
    gen_ind=0

    for i in range(len(text_list_0)):
        
               
        if(text_list_0[i].lower().find("date of birth")>-1 or text_list_0[i].lower().find("year of birth")>-1 or text_list_0[i].lower().find(" dob ") >-1 or text_list_0[i].find('DOB')>-1):
            dob=text_list_0[i]
            date_index=i            #date to be extracted later specifically   
        if(bool(re.search("\WMALE",text_list_0[i]))==True or bool(re.search("\WMale",text_list_0[i]))==True):
            gender="MALE"
            gen_ind=i
        elif(bool(re.search("FEMALE",text_list_0[i]))==True or bool(re.search("Female",text_list_0[i]))==True):
            gender="FEMALE"
            gen_ind=i    
        if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",text_list_0[i]))==True):
            aadhar_no=text_list_0[i]
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")        
    try:
        name=text_list_0[date_index-1]
        if(name.find("MALE")>-1 or name.find("Male")>-1 or name.find("Female")>-1):
            name=text_list_0[date_index-2]
    except:
        if(gen_ind>0):
            dob=text_list_0[gen_ind-1]
            name=text_list_0[gen_ind-2]        
        else:
            pass        
    fin_res={"Name":name,"DOB":dob,"GENDER":gender,"Aadhar_no":aadhar_no}

    return(fin_res)        
def aadhar_front2_template(text_list_0):
   
    #print(text_list)
    name=''
    dob=''
    gender=''
    aadhar_no=''
    gen_ind=0

    for i in range(len(text_list_0)):
        
               
        if(text_list_0[i].lower().find("date of birth")>-1 or text_list_0[i].lower().find("year of birth")>-1 or text_list_0[i].lower().find(" dob ") >-1 or text_list_0[i].find('DOB')>-1):
            dob=text_list_0[i]
            date_index=i            #date to be extracted later specifically   
        if(bool(re.search("\WMALE",text_list_0[i]))==True or bool(re.search("\WMale",text_list_0[i]))==True):
            gender="MALE"
            gen_ind=i
        elif(bool(re.search("FEMALE",text_list_0[i]))==True or bool(re.search("Female",text_list_0[i]))==True):
            gender="FEMALE"
            gen_ind=i    
        if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",text_list_0[i]))==True):
            aadhar_no=text_list_0[i]
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")        
    try:
        name=text_list_0[date_index-1]
        if(name.find("MALE")>-1 or name.find("Male")>-1 or name.find("Female")>-1):
            name=text_list_0[date_index-2]
    except:
        if(gen_ind>0):
            dob=text_list_0[gen_ind-1]
            name=text_list_0[gen_ind-2]        
        else:
            pass        
    fin_res={"Name":name,"DOB":dob,"GENDER":gender,"Aadhar_no":aadhar_no}

    return(fin_res)        
def aadhar_front1_template(text_list_0):
   
    #print(text_list)
    name=''
    dob=''
    gender=''
    aadhar_no=''
    gen_ind=0

    for i in range(len(text_list_0)):
        
               
        if(text_list_0[i].lower().find("date of birth")>-1 or text_list_0[i].lower().find("year of birth")>-1 or text_list_0[i].lower().find(" dob ") >-1 or text_list_0[i].find('DOB')>-1):
            dob=text_list_0[i]
            date_index=i            #date to be extracted later specifically   
        if(bool(re.search("\WMALE",text_list_0[i]))==True or bool(re.search("\WMale",text_list_0[i]))==True):
            gender="MALE"
            gen_ind=i
        elif(bool(re.search("FEMALE",text_list_0[i]))==True or bool(re.search("Female",text_list_0[i]))==True):
            gender="FEMALE"
            gen_ind=i    
        if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",text_list_0[i]))==True):
            aadhar_no=text_list_0[i]
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")        
    try:
        name=text_list_0[date_index-1]
        if(name.find("MALE")>-1 or name.find("Male")>-1 or name.find("Female")>-1):
            name=text_list_0[date_index-2]
    except:
        if(gen_ind>0):
            dob=text_list_0[gen_ind-1]
            name=text_list_0[gen_ind-2]        
        else:
            pass        
    fin_res={"Name":name,"DOB":dob,"GENDER":gender,"Aadhar_no":aadhar_no}

    return(fin_res)        
def aadhar_front0_template(text_list_0):
   
    #print(text_list)
    name=''
    dob=''
    gender=''
    aadhar_no=''
    gen_ind=0

    for i in range(len(text_list_0)):
        
               
        if(text_list_0[i].lower().find("date of birth")>-1 or text_list_0[i].lower().find("year of birth")>-1 or text_list_0[i].lower().find(" dob ") >-1 or text_list_0[i].find('DOB')>-1):
            dob=text_list_0[i]
            date_index=i            #date to be extracted later specifically   
        if(bool(re.search("\WMALE",text_list_0[i]))==True or bool(re.search("\WMale",text_list_0[i]))==True):
            gender="MALE"
            gen_ind=i
        elif(bool(re.search("FEMALE",text_list_0[i]))==True or bool(re.search("Female",text_list_0[i]))==True):
            gender="FEMALE"
            gen_ind=i    
        if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",text_list_0[i]))==True):
            aadhar_no=text_list_0[i]
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")        
    try:
        name=text_list_0[date_index-1]
        if(name.find("MALE")>-1 or name.find("Male")>-1 or name.find("Female")>-1):
            name=text_list_0[date_index-2]
    except:
        if(gen_ind>0):
            dob=text_list_0[gen_ind-1]
            name=text_list_0[gen_ind-2]        
        else:
            pass        
    fin_res={"Name":name,"DOB":dob,"GENDER":gender,"Aadhar_no":aadhar_no}

    return(fin_res)        


def pan0_template(text_list):
    name=''
    fathers_name=''
    dob=''
    pan_no=''
    for i in range(len(text_list)):
        '''if(text_list[i].replace(" ","").replace("/","").replace("\\","").isdigit() and (len(text_list[i])>=4 or len(text_list[i])<=8)):
            dob=text_list[i]
            fathers_name=text_list[i-1]
            name=text_list[i-2]'''
            

        if(text_list[i].replace(" ","").isalnum() and len(text_list[i].replace(" ",""))==10):
            pan_no=text_list[i]   
            dob=text_list[i-2]
            fathers_name=text_list[i-3]
            name=text_list[i-4] 
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")        
    fin_res={"Name":name,"Fathers_name":fathers_name,"DOB":dob,"Pan_no":pan_no}

    return(fin_res)
def pan1_template(text_list):
    name=''
    fathers_name=''
    dob=''
    pan_no=''
    for i in range(len(text_list)):
        if(text_list[i].lower().find("name")>-1 and (text_list[i].lower().find("father")==-1 and text_list[i].lower().find("mother")==-1)):
            name=text_list[i+1]
        if(text_list[i].lower().find("father")>-1 or text_list[i].lower().find("mother")>-1) and (text_list[i].lower().find("name")>-1):
            fathers_name=text_list[i+1]
        if(text_list[i].lower().find("date of birth")>-1):
            dob=text_list[i+1]    
        if(text_list[i].replace(" ","").isalnum() and len(text_list[i].replace(" ",""))==10):
            pan_no=text_list[i]        
    fin_res={"Name":name,"Fathers_name":fathers_name,"DOB":dob,"Pan_no":pan_no}
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")
    return(fin_res)  
def pan2_template(text_list):
    name=''
    fathers_name=''
    dob=''
    pan_no=''
    for i in range(len(text_list)):
        if(text_list[i].lower().find("name")>-1 and (text_list[i].lower().find("father")==-1 and text_list[i].lower().find("mother")==-1)):
            name=text_list[i+1]
        if(text_list[i].lower().find("father")>-1 or text_list[i].lower().find("mother")>-1) and (text_list[i].lower().find("name")>-1):
            fathers_name=text_list[i+1]
        if(text_list[i].lower().find("date of birth")>-1):
            dob=text_list[i+1]    
        if(text_list[i].replace(" ","").isalnum() and len(text_list[i].replace(" ",""))==10):
            pan_no=text_list[i]        
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")
    fin_res={"Name":name,"Fathers_name":fathers_name,"DOB":dob,"Pan_no":pan_no}
    return(fin_res)  
def aadhar_back0_template(text_list):
    addlist=[]
    house_no,building_name,street,locality,city,state,country,pin_code='','','','','','','',''
    country="India"
    for i in range(len(text_list)):
        if(text_list[i].lower().find("address")>-1):
         text_list[i]=text_list[i].lower().replace("address","").replace(":","")
         addlist=text_list[i:]
         break
         
    for i in range(len(addlist)):

        if(bool(re.search(" \d\d\d\d\d\d ",addlist[i].lower()))==True):
            addlist=addlist[:i+1]
            break 
    #-------------------------------google maps results -----------------------------------
    params = {'address': str(addlist),'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
    jsonfromgoogle = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
    dfgoogle = pd.read_json(jsonfromgoogle.text)
    strgoogle = dfgoogle['results']
    addgoogle = str(strgoogle[0]['formatted_address'])
    addgoogle = addgoogle.split(",")
    tempstate = addgoogle[len(addgoogle)-2]
    state=''
    gpin=''
    for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
    city=addgoogle[len(addgoogle)-3]
    pin_code=gpin
    #print(addgoogle,"ADD FROM GOOGLE")
    rem_addstr=str(addlist)
    rem_addstr=rem_addstr.replace("  ","")
    for i in range(2,len(state)):
        if(state[i].isupper()):
            state=state[:i]+" "+state[i:]
            break
    rem_addstr=rem_addstr.replace(city,"").replace(state,"").replace(pin_code.replace(" ",''),"").replace("pin code","").replace(" state ","")
    listdf=rem_addstr.split(",")
    for i in range(len(listdf)):
                tempo=listdf[i].lower()
                if (tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1 or tempo.find("so:")>-1 or tempo.find("do:")>-1 or tempo.find("co:")>-1):
                    listdf = listdf[i+1:]
                    break
    for i in range(len(listdf)):
       listdf[i]=listdf[i].replace("'","").replace("-","").replace(":","").replace("  ","").replace(".",'').replace("[","").replace("]","")
    for i in range(0,4):
                if(listdf[i].replace(" ", "").isalpha()==False or listdf[i].replace(" ","").isdigit()==True):
                        house_no=listdf[i]
                        listdf=listdf[i+1:]
                        break
    x=len(listdf)-1            
    while x>=0:
        if(len(listdf[x])<2):
            listdf.pop(x)
        x-=1
    ##print(type(addgoogle))
    ##print(addgoogle)
    latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
    lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])
    ##print(latgoogle,lnggoogle)    
    #-----------------------------------processing according to logic------------------------------------{PACKING_VALUES}
    listdf1=listdf.copy()
    listdf1.insert(0,house_no)
    listdf1.append(city)
    listdf1.append(state)
    listdf1.append(country)
    lent=0
    for lst in listdf1:
        lent=lent+len(lst)
    

    if(lent>120):
        for i in range(len(listdf1)):            #to remove starting spaces
            if(listdf1[i].startswith(" ")):
                listdf1[i]=listdf1[i][1:]
        
        
        for i in range(len(listdf1)-3):
            if(listdf1[i].find(city)>-1 or listdf1[i].find(state)>-1 or listdf1[i].find(country)>-1 or listdf1[i].lower().find("district")>-1 or listdf1[i].find("State")>-1 or listdf1[i].lower().find("country")>-1):
                listdf1[i]=''
        x=len(listdf1)-1
        while x>=0:
            if(listdf1[x]==''):
                listdf1.pop(x)
            x=x-1    
        lent=0
        for lst in listdf1:
            lent=lent+len(lst)              
        if(lent>120):
            building_name=listdf1[1]
            locality=addgoogle[2]
            street=addgoogle[1]
            xxx=-1
            logging.info("NOT ABLE TO SET MIN LENGTH, USING GOOGLE PLACES ")
        else:
            listdf1=listdf1[1:len(listdf1)-3]
            listdf=listdf1.copy()        
            logging.info("NO OF CHARS NOW BELOW 120 ..... now appending as per logic")   
            xxx = len(listdf)      
    else:
        xxx=len(listdf)             
    if(xxx==0):
        locality = ''
        street = ''
        building_name = ''
    elif (xxx == 1 ):
        locality = listdf[0]
        street = ''
        building_name = ''

    elif (xxx == 2):
        locality = listdf[1]
        street = ''
        building_name = listdf[0]
    elif (xxx == 3):
        locality = listdf[2]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 4):
        locality = listdf[2]+listdf[3]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 5):
        locality = listdf[3]+listdf[4]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 6):
        locality = listdf[3]+listdf[4]+listdf[5]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 7):
        locality = listdf[4]+listdf[5]+listdf[6]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 8):
        locality = listdf[4]+listdf[5]+listdf[6]+listdf[7]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 9):
        locality = listdf[5]+listdf[6]+listdf[7]+listdf[8]
        street = listdf[1]+listdf[2]+listdf[3]+listdf[4]
        building_name = listdf[0]
    
    if(len(locality)>39  or  len(street)>39  or len(building_name)>39):
            logging.info("FIRST PASS")
            if (xxx == 6):
                locality = listdf[4]+listdf[5]
                street = listdf[2]+listdf[3]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[5]+listdf[6]
                street = listdf[2]+listdf[3]+listdf[4]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[3]+listdf[4]+listdf[5]
                building_name = listdf[0]+listdf[1]+listdf[2]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[4]+listdf[5]+listdf[6]
                building_name = listdf[0]+listdf[1]+listdf[2]+listdf[3]
    if(len(building_name)>39 or len(street)>39 or len(locality)>39):
            logging.info("SECOND PASS")
            if (xxx == 6):
                locality = listdf[5]
                street = listdf[4]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[6]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[5]+listdf[6]
                building_name = listdf[3]+listdf[4]
                house_no=house_no+listdf[0]+listdf[1]+listdf[2]
    if(len(house_no)>39 or len(building_name)>39 or len(locality)>39 or len(street)>39):
        logging.info("PASS 3 TRIM")
        house_no=list(house_no[:39])
        house_no="".join(house_no)
        building_name=list(building_name[:39])
        building_name="".join(building_name)
        locality=list(locality[:39])
        locality="".join(locality)
        street=list(street[:39])
        street="".join(street)
    if(len(pin_code)<6 or str(pin_code).replace(" ","").isdigit==False):
        pin_code=listdf[len(listdf)-1]

    addfinal = {"House_no": house_no, "Building_name": building_name, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pin_code, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle,"status_code":1,"status_message":"SUCCESS"}
    return(addfinal)
def aadhar_back1_template(text_list):
    addlist=[]
    house_no,building_name,street,locality,city,state,country,pin_code='','','','','','','',''
    country="India"
    for i in range(len(text_list)):
        if(text_list[i].lower().find("address")>-1):
         text_list[i]=text_list[i].lower().replace("address","").replace(":","")
         addlist=text_list[i:]
         break
         
    for i in range(len(addlist)):

        if(bool(re.search(" \d\d\d\d\d\d ",addlist[i].lower()))==True):
            addlist=addlist[:i+1]
            break 
    #-------------------------------google maps results -----------------------------------
    params = {'address': str(addlist),'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
    jsonfromgoogle = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
    dfgoogle = pd.read_json(jsonfromgoogle.text)
    strgoogle = dfgoogle['results']
    addgoogle = str(strgoogle[0]['formatted_address'])
    addgoogle = addgoogle.split(",")
    tempstate = addgoogle[len(addgoogle)-2]
    state=''
    gpin=''
    for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
    city=addgoogle[len(addgoogle)-3]
    pin_code=gpin
    #print(addgoogle,"ADD FROM GOOGLE")
    rem_addstr=str(addlist)
    rem_addstr=rem_addstr.replace("  ","")
    for i in range(2,len(state)):
        if(state[i].isupper()):
            state=state[:i]+" "+state[i:]
            break
    rem_addstr=rem_addstr.replace(city,"").replace(state,"").replace(pin_code.replace(" ",''),"").replace("pin code","").replace(" state ","")
    listdf=rem_addstr.split(",")
    for i in range(len(listdf)):
                tempo=listdf[i].lower()
                if (tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1 or tempo.find("so:")>-1 or tempo.find("do:")>-1 or tempo.find("co:")>-1):
                    listdf = listdf[i+1:]
                    break
    for i in range(len(listdf)):
       listdf[i]=listdf[i].replace("'","").replace("-","").replace(":","").replace("  ","").replace(".",'').replace("[","").replace("]","")
    for i in range(0,4):
                if((listdf[i].replace(" ", "").isalpha()==False) or (listdf[i].replace(" ","").isdigit()==True)):
                    house_no=listdf[i]
                    listdf=listdf[i+1:]
                    break
    x=len(listdf)-1            
    while x>=0:
        if(len(listdf[x])<2):
            listdf.pop(x)
        x-=1
    ##print(type(addgoogle))
    ##print(addgoogle)
    latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
    lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])
    ##print(latgoogle,lnggoogle)    
    #-----------------------------------processing according to logic------------------------------------{PACKING_VALUES}
    listdf1=listdf.copy()
    listdf1.insert(0,house_no)
    listdf1.append(city)
    listdf1.append(state)
    listdf1.append(country)
    lent=0
    for lst in listdf1:
        lent=lent+len(lst)
    

    if(lent>120):
        for i in range(len(listdf1)):            #to remove starting spaces
            if(listdf1[i].startswith(" ")):
                listdf1[i]=listdf1[i][1:]
        
        
        for i in range(len(listdf1)-3):
            if(listdf1[i].find(city)>-1 or listdf1[i].find(state)>-1 or listdf1[i].find(country)>-1 or listdf1[i].lower().find("district")>-1 or listdf1[i].find("State")>-1 or listdf1[i].lower().find("country")>-1):
                listdf1[i]=''
        x=len(listdf1)-1
        while x>=0:
            if(listdf1[x]==''):
                listdf1.pop(x)
            x=x-1    
        lent=0
        for lst in listdf1:
            lent=lent+len(lst)              
        if(lent>120):
            building_name=listdf1[1]
            locality=addgoogle[2]
            street=addgoogle[1]
            xxx=-1
            logging.info("NOT ABLE TO SET MIN LENGTH, USING GOOGLE PLACES ")
        else:
            listdf1=listdf1[1:len(listdf1)-3]
            listdf=listdf1.copy()        
            logging.info("NO OF CHARS NOW BELOW 120 ..... now appending as per logic")   
            xxx = len(listdf)      
    else:
        xxx=len(listdf)             
    if(xxx==0):
        locality = ''
        street = ''
        building_name = ''
    elif (xxx == 1 ):
        locality = listdf[0]
        street = ''
        building_name = ''

    elif (xxx == 2):
        locality = listdf[1]
        street = ''
        building_name = listdf[0]
    elif (xxx == 3):
        locality = listdf[2]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 4):
        locality = listdf[2]+listdf[3]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 5):
        locality = listdf[3]+listdf[4]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 6):
        locality = listdf[3]+listdf[4]+listdf[5]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 7):
        locality = listdf[4]+listdf[5]+listdf[6]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 8):
        locality = listdf[4]+listdf[5]+listdf[6]+listdf[7]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 9):
        locality = listdf[5]+listdf[6]+listdf[7]+listdf[8]
        street = listdf[1]+listdf[2]+listdf[3]+listdf[4]
        building_name = listdf[0]
    
    if(len(locality)>39  or  len(street)>39  or len(building_name)>39):
            logging.info("FIRST PASS")
            if (xxx == 6):
                locality = listdf[4]+listdf[5]
                street = listdf[2]+listdf[3]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[5]+listdf[6]
                street = listdf[2]+listdf[3]+listdf[4]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[3]+listdf[4]+listdf[5]
                building_name = listdf[0]+listdf[1]+listdf[2]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[4]+listdf[5]+listdf[6]
                building_name = listdf[0]+listdf[1]+listdf[2]+listdf[3]
    if(len(building_name)>39 or len(street)>39 or len(locality)>39):
            logging.info("SECOND PASS")
            if (xxx == 6):
                locality = listdf[5]
                street = listdf[4]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[6]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[5]+listdf[6]
                building_name = listdf[3]+listdf[4]
                house_no=house_no+listdf[0]+listdf[1]+listdf[2]
    if(len(house_no)>39 or len(building_name)>39 or len(locality)>39 or len(street)>39):
        logging.info("PASS 3 TRIM")
        house_no=list(house_no[:39])
        house_no="".join(house_no)
        building_name=list(building_name[:39])
        building_name="".join(building_name)
        locality=list(locality[:39])
        locality="".join(locality)
        street=list(street[:39])
        street="".join(street)
    if(len(pin_code)<6 or str(pin_code).replace(" ","").isdigit==False):
        pin_code=listdf[len(listdf)-1]    
    addfinal = {"House_no": house_no, "Building_name": building_name, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pin_code, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle,"status_code":1,"status_message":"SUCCESS"}
    return(addfinal)
def aadhar_back2_template(text_list):
    addlist=[]
    house_no,building_name,street,locality,city,state,country,pin_code='','','','','','','',''
    country="India"
    for i in range(len(text_list)):
        if(text_list[i].lower().find("address")>-1):
         text_list[i]=text_list[i].lower().replace("address","").replace(":","")
         addlist=text_list[i:]
         break
         
    for i in range(len(addlist)):

        if(bool(re.search(" \d\d\d\d\d\d ",addlist[i].lower()))==True):
            addlist=addlist[:i+1]
            break 
    #-------------------------------google maps results -----------------------------------
    params = {'address': str(addlist),'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
    jsonfromgoogle = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
    dfgoogle = pd.read_json(jsonfromgoogle.text)
    strgoogle = dfgoogle['results']
    addgoogle = str(strgoogle[0]['formatted_address'])
    addgoogle = addgoogle.split(",")
    tempstate = addgoogle[len(addgoogle)-2]
    state=''
    gpin=''
    for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
    city=addgoogle[len(addgoogle)-3]
    pin_code=gpin
    #print(addgoogle,"ADD FROM GOOGLE")
    rem_addstr=str(addlist)
    rem_addstr=rem_addstr.replace("  ","")
    for i in range(2,len(state)):
        if(state[i].isupper()):
            state=state[:i]+" "+state[i:]
            break
    rem_addstr=rem_addstr.replace(city,"").replace(state,"").replace(pin_code.replace(" ",''),"").replace("pin code","").replace(" state ","")
    listdf=rem_addstr.split(",")
    for i in range(len(listdf)):
                tempo=listdf[i].lower()
                if (tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1 or tempo.find("so:")>-1 or tempo.find("do:")>-1 or tempo.find("co:")>-1):
                    listdf = listdf[i+1:]
                    break
    for i in range(len(listdf)):
       listdf[i]=listdf[i].replace("'","").replace("-","").replace(":","").replace("  ","").replace(".",'').replace("[","").replace("]","")
    for i in range(0,4):
                if((listdf[i].replace(" ", "").isalpha()==False) or (listdf[i].replace(" ","").isdigit()==True)):
                    house_no=listdf[i]
                    listdf=listdf[i+1:]
                    break
    x=len(listdf)-1            
    while x>=0:
        if(len(listdf[x])<2):
            listdf.pop(x)
        x-=1
    ##print(type(addgoogle))
    ##print(addgoogle)
    latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
    lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])
    ##print(latgoogle,lnggoogle)    
    #-----------------------------------processing according to logic------------------------------------{PACKING_VALUES}
    listdf1=listdf.copy()
    listdf1.insert(0,house_no)
    listdf1.append(city)
    listdf1.append(state)
    listdf1.append(country)
    lent=0
    for lst in listdf1:
        lent=lent+len(lst)
    

    if(lent>120):
        for i in range(len(listdf1)):            #to remove starting spaces
            if(listdf1[i].startswith(" ")):
                listdf1[i]=listdf1[i][1:]
        
        
        for i in range(len(listdf1)-3):
            if(listdf1[i].find(city)>-1 or listdf1[i].find(state)>-1 or listdf1[i].find(country)>-1 or listdf1[i].lower().find("district")>-1 or listdf1[i].find("State")>-1 or listdf1[i].lower().find("country")>-1):
                listdf1[i]=''
        x=len(listdf1)-1
        while x>=0:
            if(listdf1[x]==''):
                listdf1.pop(x)
            x=x-1    
        lent=0
        for lst in listdf1:
            lent=lent+len(lst)              
        if(lent>120):
            building_name=listdf1[1]
            locality=addgoogle[2]
            street=addgoogle[1]
            xxx=-1
            logging.info("NOT ABLE TO SET MIN LENGTH, USING GOOGLE PLACES ")
        else:
            listdf1=listdf1[1:len(listdf1)-3]
            listdf=listdf1.copy()        
            logging.info("NO OF CHARS NOW BELOW 120 ..... now appending as per logic")   
            xxx = len(listdf)      
    else:
        xxx=len(listdf)             
    if(xxx==0):
        locality = ''
        street = ''
        building_name = ''
    elif (xxx == 1 ):
        locality = listdf[0]
        street = ''
        building_name = ''

    elif (xxx == 2):
        locality = listdf[1]
        street = ''
        building_name = listdf[0]
    elif (xxx == 3):
        locality = listdf[2]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 4):
        locality = listdf[2]+listdf[3]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 5):
        locality = listdf[3]+listdf[4]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 6):
        locality = listdf[3]+listdf[4]+listdf[5]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 7):
        locality = listdf[4]+listdf[5]+listdf[6]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 8):
        locality = listdf[4]+listdf[5]+listdf[6]+listdf[7]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 9):
        locality = listdf[5]+listdf[6]+listdf[7]+listdf[8]
        street = listdf[1]+listdf[2]+listdf[3]+listdf[4]
        building_name = listdf[0]
    
    if(len(locality)>39  or  len(street)>39  or len(building_name)>39):
            logging.info("FIRST PASS")
            if (xxx == 6):
                locality = listdf[4]+listdf[5]
                street = listdf[2]+listdf[3]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[5]+listdf[6]
                street = listdf[2]+listdf[3]+listdf[4]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[3]+listdf[4]+listdf[5]
                building_name = listdf[0]+listdf[1]+listdf[2]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[4]+listdf[5]+listdf[6]
                building_name = listdf[0]+listdf[1]+listdf[2]+listdf[3]
    if(len(building_name)>39 or len(street)>39 or len(locality)>39):
            logging.info("SECOND PASS")
            if (xxx == 6):
                locality = listdf[5]
                street = listdf[4]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[6]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[5]+listdf[6]
                building_name = listdf[3]+listdf[4]
                house_no=house_no+listdf[0]+listdf[1]+listdf[2]
    if(len(house_no)>39 or len(building_name)>39 or len(locality)>39 or len(street)>39):
        logging.info("PASS 3 TRIM")
        house_no=list(house_no[:39])
        house_no="".join(house_no)
        building_name=list(building_name[:39])
        building_name="".join(building_name)
        locality=list(locality[:39])
        locality="".join(locality)
        street=list(street[:39])
        street="".join(street)
    if(len(pin_code)<6 or str(pin_code).replace(" ","").isdigit==False):
        pin_code=listdf[len(listdf)-1]    
    addfinal = {"House_no": house_no, "Building_name": building_name, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pin_code, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle,"status_code":1,"status_message":"SUCCESS"}
    return(addfinal)               
def aadhar_strip0_template(text_list):
    text_list_0=text_list[len(text_list)//2:]
    name=''
    dob=''
    gender=''
    aadhar_no=''
    gen_ind=0
    for i in range(len(text_list_0)):
        
               
        if(text_list_0[i].lower().find("date of birth")>-1 or text_list_0[i].lower().find("year of birth")>-1 or text_list_0[i].lower().find(" dob ") >-1 or text_list_0[i].find('DOB')>-1):
            dob=text_list_0[i]
            date_index=i            #date to be extracted later specifically   
        if(bool(re.search("\WMALE",text_list_0[i]))==True or bool(re.search("\WMale",text_list_0[i]))==True):
            gender="MALE"
            gen_ind=i
        elif(bool(re.search("FEMALE",text_list_0[i]))==True or bool(re.search("Female",text_list_0[i]))==True):
            gender="FEMALE"
            gen_ind=i    
        if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",text_list_0[i]))==True):
            aadhar_no=text_list_0[i]
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")        
    try:
        name=text_list_0[date_index-1]
        if(name.find("MALE")>-1 or name.find("Male")>-1 or name.find("Female")>-1):
            name=text_list_0[date_index-2]
    except:
        if(gen_ind>0):
            dob=text_list_0[gen_ind-1]
            name=text_list_0[gen_ind-2]        
        else:
            pass
    
    fin_res={"Name":name,"DOB":dob,"GENDER":gender,"Aadhar_no":aadhar_no}
    addlist=[]
    house_no,building_name,street,locality,city,state,country,pin_code='','','','','','','',''
    country="India"
    for i in range(len(text_list)):
        if(text_list[i].lower().find("address")>-1 or text_list[i].find("To ")>-1):
         text_list[i]=text_list[i].lower().replace("address","").replace(":","").replace("To","")
         addlist=text_list[i:]
         break
         
    for i in range(len(addlist)):

        if(bool(re.search(" \d\d\d\d\d\d ",addlist[i].lower()))==True):
            addlist=addlist[:i+1]
            break 
    #-------------------------------google maps results -----------------------------------
    params = {'address': str(addlist),'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
    jsonfromgoogle = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
    dfgoogle = pd.read_json(jsonfromgoogle.text)
    strgoogle = dfgoogle['results']
    addgoogle = str(strgoogle[0]['formatted_address'])
    addgoogle = addgoogle.split(",")
    tempstate = addgoogle[len(addgoogle)-2]
    state=''
    gpin=''
    for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
    city=addgoogle[len(addgoogle)-3]
    pin_code=gpin
    #print(addgoogle,"ADD FROM GOOGLE")
    rem_addstr=str(addlist)
    rem_addstr=rem_addstr.replace("  ","")
    for i in range(2,len(state)):
        if(state[i].isupper()):
            state=state[:i]+" "+state[i:]
            break
    rem_addstr=rem_addstr.replace(city,"").replace(state,"").replace(pin_code.replace(" ",''),"").lower().replace("pin code","").replace(" state ","")
    listdf=rem_addstr.split(",")
    for i in range(len(listdf)):
                tempo=listdf[i].lower()
                if (tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1 or tempo.find("so:")>-1 or tempo.find("do:")>-1 or tempo.find("co:")>-1):
                    listdf = listdf[i+1:]
                    break
    for i in range(len(listdf)):
       listdf[i]=listdf[i].replace("'","").replace("-","").replace(":","").replace("  ","").replace(".",'').replace("[","").replace("]","")
    for i in range(0,4):
                if(listdf[i].replace(" ", "").isalpha()==False or listdf[i].replace(" ","").isdigit()==True):
                        house_no=listdf[i]
                        listdf=listdf[i+1:]
                        break
    x=len(listdf)-1            
    while x>=0:
        if(len(listdf[x])<2):
            listdf.pop(x)
        x-=1
    ##print(type(addgoogle))
    ##print(addgoogle)
    latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
    lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])
    ##print(latgoogle,lnggoogle)    
    #-----------------------------------processing according to logic------------------------------------{PACKING_VALUES}
    listdf1=listdf.copy()
    listdf1.insert(0,house_no)
    listdf1.append(city)
    listdf1.append(state)
    listdf1.append(country)
    lent=0
    for lst in listdf1:
        lent=lent+len(lst)
    

    if(lent>120):
        for i in range(len(listdf1)):            #to remove starting spaces
            if(listdf1[i].startswith(" ")):
                listdf1[i]=listdf1[i][1:]
        
        
        for i in range(len(listdf1)-3):
            if(listdf1[i].find(city)>-1 or listdf1[i].find(state)>-1 or listdf1[i].find(country)>-1 or listdf1[i].lower().find("district")>-1 or listdf1[i].find("State")>-1 or listdf1[i].lower().find("country")>-1):
                listdf1[i]=''
        x=len(listdf1)-1
        while x>=0:
            if(listdf1[x]==''):
                listdf1.pop(x)
            x=x-1    
        lent=0
        for lst in listdf1:
            lent=lent+len(lst)              
        if(lent>120):
            building_name=listdf1[1]
            locality=addgoogle[2]
            street=addgoogle[1]
            xxx=-1
            logging.info("NOT ABLE TO SET MIN LENGTH, USING GOOGLE PLACES ")
        else:
            listdf1=listdf1[1:len(listdf1)-3]
            listdf=listdf1.copy()        
            logging.info("NO OF CHARS NOW BELOW 120 ..... now appending as per logic")   
            xxx = len(listdf)      
    else:
        xxx=len(listdf)             
    if(xxx==0):
        locality = ''
        street = ''
        building_name = ''
    elif (xxx == 1 ):
        locality = listdf[0]
        street = ''
        building_name = ''

    elif (xxx == 2):
        locality = listdf[1]
        street = ''
        building_name = listdf[0]
    elif (xxx == 3):
        locality = listdf[2]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 4):
        locality = listdf[2]+listdf[3]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 5):
        locality = listdf[3]+listdf[4]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 6):
        locality = listdf[3]+listdf[4]+listdf[5]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 7):
        locality = listdf[4]+listdf[5]+listdf[6]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 8):
        locality = listdf[4]+listdf[5]+listdf[6]+listdf[7]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 9):
        locality = listdf[5]+listdf[6]+listdf[7]+listdf[8]
        street = listdf[1]+listdf[2]+listdf[3]+listdf[4]
        building_name = listdf[0]
    
    if(len(locality)>39  or  len(street)>39  or len(building_name)>39):
            logging.info("FIRST PASS")
            if (xxx == 6):
                locality = listdf[4]+listdf[5]
                street = listdf[2]+listdf[3]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[5]+listdf[6]
                street = listdf[2]+listdf[3]+listdf[4]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[3]+listdf[4]+listdf[5]
                building_name = listdf[0]+listdf[1]+listdf[2]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[4]+listdf[5]+listdf[6]
                building_name = listdf[0]+listdf[1]+listdf[2]+listdf[3]
    if(len(building_name)>39 or len(street)>39 or len(locality)>39):
            logging.info("SECOND PASS")
            if (xxx == 6):
                locality = listdf[5]
                street = listdf[4]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[6]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[5]+listdf[6]
                building_name = listdf[3]+listdf[4]
                house_no=house_no+listdf[0]+listdf[1]+listdf[2]
    if(len(house_no)>39 or len(building_name)>39 or len(locality)>39 or len(street)>39):
        logging.info("PASS 3 TRIM")
        house_no=list(house_no[:39])
        house_no="".join(house_no)
        building_name=list(building_name[:39])
        building_name="".join(building_name)
        locality=list(locality[:39])
        locality="".join(locality)
        street=list(street[:39])
        street="".join(street)
    if(len(pin_code)<6 or str(pin_code).replace(" ","").isdigit==False):
        pin_code=listdf[len(listdf)-1]

    addfinal = {"House_no": house_no, "Building_name": building_name, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pin_code, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle}
    addfinal.update(fin_res)
    return(addfinal)
def aadhar_full0_template(image_path,text_list):
   
    img=cv2.imread(image_path)
    h,w,_=img.shape
    print("HERE OK 1 ",h,w)
    
    left_lines=[]
    right_lines=[]
    print("RUNNING TILL HERE a")
    
    
    for i in text_list:
          if(type(i[0])==dict):
           i.pop(0) 
    for i in text_list:      
          if(type(i[0])==dict):
           i.pop(0) 
          if(i[0][0][0][0]<w//3):
               left_lines.append(i)
               #print("LEFT")
               print("RUNNING TILL HERE ab")
          else:
               right_lines.append(i)
               print("RUNNING TILL HERE ac")    
               #print("RIGHT")
    
    print("RUNNING TILL HERE b")
    uriidentifier=[]
    for i in range(len(left_lines)):
       stro=''
       for j in range(len(left_lines[i])):
                        
           #print(left_lines[i][j][1]["t_"],end=" ")
           stro=stro+left_lines[i][j][1]["t_"]+" "
       uriidentifier.append(stro)
       #print("\n")
    for i in range(len(right_lines)):
       stro=''
       for j in range(len(right_lines[i])):
                        
           #print(right_lines[i][j][1]["t_"],end=" ")
           stro=stro+right_lines[i][j][1]["t_"]+" "
       uriidentifier.append(stro)
       #print("\n")
    
    #text_list_0=uriidentifier[len(uriidentifier)//6:]
    name=''
    dob=''
    gender=''
    aadhar_no=''
    for i in uriidentifier:
        print(i)
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")    
    for i in range(len(uriidentifier)):
        if(uriidentifier[i].lower().find("government of india")>-1 ):
            text_list_0=uriidentifier[i+1:]
            break

    for i in range(len(text_list_0)):
        print(text_list_0[i])
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")                
    for i in range(len(text_list_0)):
        if(text_list_0[i].lower().find("government of india")>-1 ):        
            for j in range(i,len(text_list_0)):
                if(text_list_0[j].find("INFORMATION")>-1):
                    text_list_0=text_list_0[i:j]
                    break
            break
    for i in range(len(text_list_0)):
        print(text_list_0[i])    
    gen_ind=0
    for i in range(len(text_list_0)):
        
               
        if(text_list_0[i].lower().find("date of birth")>-1 or text_list_0[i].lower().find("year of birth")>-1 or text_list_0[i].lower().find(" dob ") >-1 or text_list_0[i].find('DOB')>-1):
            dob=text_list_0[i]
            date_index=i            #date to be extracted later specifically   
        if(bool(re.search("\WMALE",text_list_0[i]))==True or bool(re.search("\WMale",text_list_0[i]))==True):
            gender="MALE"
            gen_ind=i
        elif(bool(re.search("FEMALE",text_list_0[i]))==True or bool(re.search("Female",text_list_0[i]))==True):
            gender="FEMALE"
            gen_ind=i    
        if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",text_list_0[i]))==True):
            aadhar_no=text_list_0[i]
    dob=dob.lower().replace("dob","").replace(":","").replace("year of birth","")        
    try:
        name=text_list_0[date_index-1]
        if(name.find("MALE")>-1 or name.find("Male")>-1 or name.find("Female")>-1):
            name=text_list_0[date_index-2]
    except:
        if(gen_ind>0):
            dob=text_list_0[gen_ind-1]
            name=text_list_0[gen_ind-2]        
        else:
            pass

    fin_res={"Name":name,"DOB":dob,"GENDER":gender,"Aadhar_no":aadhar_no}
    
    addlist=[]
    house_no,building_name,street,locality,city,state,country,pin_code='','','','','','','',''
    country="India"
    print("HERE OK 2")
    for i in range(len(uriidentifier)):
        if(uriidentifier[i].lower().find("to ")>-1 ):
         uriidentifier[i]=uriidentifier[i].lower().replace("address","").replace(":","").replace("to ",'')
         addlist=uriidentifier[i:]
         break
         
    for i in range(len(addlist)):

        if(bool(re.search(" \d\d\d\d\d\d ",addlist[i].lower()))==True):
            addlist=addlist[:i+1]
            break 
    #-------------------------------google maps results -----------------------------------
    params = {'address': str(addlist),'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
    jsonfromgoogle = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
    dfgoogle = pd.read_json(jsonfromgoogle.text)
    strgoogle = dfgoogle['results']
    addgoogle = str(strgoogle[0]['formatted_address'])
    addgoogle = addgoogle.split(",")
    tempstate = addgoogle[len(addgoogle)-2]
    state=''
    gpin=''
    for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
    city=addgoogle[len(addgoogle)-3]
    pin_code=gpin
    #print(addgoogle,"ADD FROM GOOGLE")
    rem_addstr=str(addlist)
    rem_addstr=rem_addstr.replace("  ","")
    for i in range(2,len(state)):
        if(state[i].isupper()):
            state=state[:i]+" "+state[i:]
            break
    rem_addstr=rem_addstr.replace(city,"").replace(state,"").replace(pin_code.replace(" ",''),"").lower().replace("pin code","").replace(" state ","")
    listdf=rem_addstr.split(",")
    for i in range(len(listdf)):
                tempo=listdf[i].lower()
                if (tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1 or tempo.find("so:")>-1 or tempo.find("do:")>-1 or tempo.find("co:")>-1):
                    listdf = listdf[i+1:]
                    break
    for i in range(len(listdf)):
       listdf[i]=listdf[i].replace("'","").replace("-","").replace(":","").replace("  ","").replace(".",'').replace("[","").replace("]","")
    for i in range(0,4):
                if(listdf[i].replace(" ", "").isalpha()==False or listdf[i].replace(" ","").isdigit()==True):
                        house_no=listdf[i]
                        listdf=listdf[i+1:]
                        break
    x=len(listdf)-1            
    while x>=0:
        if(len(listdf[x])<2):
            listdf.pop(x)
        x-=1
    ##print(type(addgoogle))
    ##print(addgoogle)
    latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
    lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])
    ##print(latgoogle,lnggoogle)    
    #-----------------------------------processing according to logic------------------------------------{PACKING_VALUES}
    listdf1=listdf.copy()
    listdf1.insert(0,house_no)
    listdf1.append(city)
    listdf1.append(state)
    listdf1.append(country)
    lent=0
    for lst in listdf1:
        lent=lent+len(lst)
    

    if(lent>120):
        for i in range(len(listdf1)):            #to remove starting spaces
            if(listdf1[i].startswith(" ")):
                listdf1[i]=listdf1[i][1:]
        
        
        for i in range(len(listdf1)-3):
            if(listdf1[i].find(city)>-1 or listdf1[i].find(state)>-1 or listdf1[i].find(country)>-1 or listdf1[i].lower().find("district")>-1 or listdf1[i].find("State")>-1 or listdf1[i].lower().find("country")>-1):
                listdf1[i]=''
        x=len(listdf1)-1
        while x>=0:
            if(listdf1[x]==''):
                listdf1.pop(x)
            x=x-1    
        lent=0
        for lst in listdf1:
            lent=lent+len(lst)              
        if(lent>120):
            building_name=listdf1[1]
            locality=addgoogle[2]
            street=addgoogle[1]
            xxx=-1
            logging.info("NOT ABLE TO SET MIN LENGTH, USING GOOGLE PLACES ")
        else:
            listdf1=listdf1[1:len(listdf1)-3]
            listdf=listdf1.copy()        
            logging.info("NO OF CHARS NOW BELOW 120 ..... now appending as per logic")   
            xxx = len(listdf)      
    else:
        xxx=len(listdf)             
    if(xxx==0):
        locality = ''
        street = ''
        building_name = ''
    elif (xxx == 1 ):
        locality = listdf[0]
        street = ''
        building_name = ''

    elif (xxx == 2):
        locality = listdf[1]
        street = ''
        building_name = listdf[0]
    elif (xxx == 3):
        locality = listdf[2]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 4):
        locality = listdf[2]+listdf[3]
        street = listdf[1]
        building_name = listdf[0]
    elif (xxx == 5):
        locality = listdf[3]+listdf[4]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 6):
        locality = listdf[3]+listdf[4]+listdf[5]
        street = listdf[1]+listdf[2]
        building_name = listdf[0]
    elif (xxx == 7):
        locality = listdf[4]+listdf[5]+listdf[6]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 8):
        locality = listdf[4]+listdf[5]+listdf[6]+listdf[7]
        street = listdf[1]+listdf[2]+listdf[3]
        building_name = listdf[0]
    elif (xxx == 9):
        locality = listdf[5]+listdf[6]+listdf[7]+listdf[8]
        street = listdf[1]+listdf[2]+listdf[3]+listdf[4]
        building_name = listdf[0]
    
    if(len(locality)>39  or  len(street)>39  or len(building_name)>39):
            logging.info("FIRST PASS")
            if (xxx == 6):
                locality = listdf[4]+listdf[5]
                street = listdf[2]+listdf[3]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[5]+listdf[6]
                street = listdf[2]+listdf[3]+listdf[4]
                building_name = listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[3]+listdf[4]+listdf[5]
                building_name = listdf[0]+listdf[1]+listdf[2]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[4]+listdf[5]+listdf[6]
                building_name = listdf[0]+listdf[1]+listdf[2]+listdf[3]
    if(len(building_name)>39 or len(street)>39 or len(locality)>39):
            logging.info("SECOND PASS")
            if (xxx == 6):
                locality = listdf[5]
                street = listdf[4]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 7):
                locality = listdf[6]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 8):
                locality = listdf[6]+listdf[7]
                street = listdf[4]+listdf[5]
                building_name = listdf[2]+listdf[3]
                house_no=house_no+listdf[0]+listdf[1]
            elif (xxx == 9):
                locality = listdf[7]+listdf[8]
                street = listdf[5]+listdf[6]
                building_name = listdf[3]+listdf[4]
                house_no=house_no+listdf[0]+listdf[1]+listdf[2]
    if(len(house_no)>39 or len(building_name)>39 or len(locality)>39 or len(street)>39):
        logging.info("PASS 3 TRIM")
        house_no=list(house_no[:39])
        house_no="".join(house_no)
        building_name=list(building_name[:39])
        building_name="".join(building_name)
        locality=list(locality[:39])
        locality="".join(locality)
        street=list(street[:39])
        street="".join(street)
    if(len(pin_code)<6 or str(pin_code).replace(" ","").isdigit==False):
        pin_code=listdf[len(listdf)-1]

    addfinal = {"House_no": house_no, "Building_name": building_name, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pin_code, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle}
    addfinal.update(fin_res)
    print("HERE OK 3")
    return(addfinal)
   
def make_right_code_run(image_path,text_list,final_list,results):
   try:
    list_templates=['aadhar_back0.txt', 'aadhar_back1.txt', 'aadhar_back2.txt', 'aadhar_front0.txt', 'aadhar_front1.txt', 'aadhar_front2.txt', 'aadhar_front3.txt', 'aadhar_front4.txt', 'aadhar_full0.txt', 'aadhar_strip0.txt', 'pan0.txt', 'pan1.txt', 'pan2.txt']
    #print(list_templates)
    if(results.find("aadhar_full")>-1):
        fin_res=eval(results)(image_path,final_list)
    elif(str(list_templates).find(results.replace("_template",""))>-1):
        #print("FOUND")
        fin_res=eval(results)(text_list)        #converts the string to a function   
    else:
        x=x/0   #HERE THE GENERIC CODES WILL BE RUN FOR EACH 
   except Exception as e:
    
    fin_res={"ERROR":"PLZ TRY AGAIN","ERROR_CODE":str(e)}     
    
   return fin_res  #this is the final dictionary to be shown in the browser   
def imagesave(image_path):
    x=cv2.imread(image_path)
    cv2.imwrite("image_jukebox/"+image_path,x)
    os.remove(image_path)
    image_path=image_path.split(".")
    image_path[1]=".txt"
    os.remove("".join(image_path))
    os.remove("file1.txt")
    try:
        os.remove(image_path[0]+".pdf")
    except:
        pass    
#FLASK CODE WILL START FROM HERE IN THE FUTURE 

#app=Flask(__name__,root_path="/test")

app=Flask(__name__)
i=0
@app.route("/test",methods=['GET','POST'])
def photoupd():
    
    if (request.method == "POST"):
        image_path = request.files["upd"]
        cur_time=str(datetime.datetime.now().second) + str(datetime.datetime.now().microsecond)
        if(image_path.filename.find(".pdf")>-1):
            image_path.save(cur_time+".pdf")
            doc=fitz.open(cur_time+".pdf")
            page=doc[0]
            xoxo=cur_time+".pdf"
            img=page.get_pixmap(dpi=200)
                    
            xoxo=xoxo.replace(".pdf",".jpg")
            img.save(xoxo)
              
            return(xoxo)
        else:
            image_path.save(cur_time+".jpg")
            
            return(cur_time+".jpg")
    return render_template("input.html")

@app.route("/test/results",methods=['GET','POST'])
def mainfunc():
    
 try:   
    image_path=photoupd()
    
    word_list_sorted1=retsortedwords(image_path)
    image_path=rotate_image(word_list_sorted1,image_path)
    word_list_sorted=retsortedwords2(image_path)
    print("***********************************************************\n\n\n")
    
    fina_list=columnar_new(image_path,word_list_sorted)
    print("***********************************************************\n\n\n")
   
    listfin=linemaker(word_list_sorted)
    print("***********************************************************\n\n\n")
    
    list_fin=lineswithcol(image_path,listfin)
    
    text_list,final_list=maketemplate(image_path,list_fin)
    print("***********************************************************\n\n\n")
    '''for i in text_list:
        print(i)'''
      
    results=elasticcode(image_path)
    print("***********************************************************\n\n\n")
    print(results)
    print(image_path)
    fin_res=make_right_code_run(image_path,text_list,final_list,results)
    print("***********************************************************\n\n\n")
    print(fin_res)
    imagesave(image_path)
    return fin_res 
 except Exception as e:  
       raise
       
   
    
     
if __name__ == "__main__":
    app.run("0.0.0.0")





