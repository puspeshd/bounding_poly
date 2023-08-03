
import cv2
from google.cloud import vision
import os
import re
import logging
from flask import Flask,request,render_template
from fileinput import filename
import requests
from bs4 import BeautifulSoup
import words2num
from flask_cors import CORS,cross_origin
import pandas as pd
from copy import copy
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'chetan.json'
client = vision.ImageAnnotatorClient()

def retsortedwords(image_path):
    with open("image_jukebox/"+image_path, 'rb') as image_file:
        content = image_file.read()

    # Creates an image object
    image = vision.Image(content=content)

    # Performs OCR on the image
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    '''desc = annotations[0].description
    print(desc.encode("utf-8"))'''


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
        print(annotation1,end="*") 
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
        #print(word_bounding_vertices[length])
        if(word_bounding_vertices[length][1]['t_']==''):
            word_bounding_vertices.pop(length)
        length=length-1
    print(len(word_bounding_vertices)," THIS IS LENGTH AFTER TRIMMING")
    return word_bounding_vertices  
def columnar_new(word_bounding_vertices) :
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
    img=cv2.imread("image_jukebox/"+image_path)
    h,w,_=img.shape
    #print(h,w)
    #exit()
    for i in column_list:
        new_list=[]
        if(i[0][0][0][0]<w//3):
                new_list.append(f"LC{x}->")
        elif(i[0][0][0][0]>w//3):
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
    print("____________________________________LEFT COLUMNS__________________________________\n\n")
    for i in range(len(left_columns)):
        left_columns[i][0]=re.sub("LC\d->",f"LC{i}->",left_columns[i][0])
        left_columns[i][0]=re.sub("LC\d\d->",f"LC{i}->",left_columns[i][0])
        print(left_columns[i])
        x.write(str(left_columns[i])+"\n")
    x.write("\n_________________________________________RIGHT COLUMNS___________________________________________\n\n")
    print("____________________________________RIGHT COLUMNS__________________________________\n\n")
    for i in range(len(right_columns)):
        right_columns[i][0]=re.sub("RC\d->",f"RC{i}->",right_columns[i][0])
        right_columns[i][0]=re.sub("RC\d\d->",f"RC{i}->",right_columns[i][0])
        print(right_columns[i])
        x.write(str(right_columns[i])+"\n") 
    x.write("\n_________________________________________CENTER COLUMNS___________________________________________\n\n")
    print("____________________________________CENTER COLUMNS__________________________________\n\n")
    for i in range(len(center_columns)):
        center_columns[i][0]=re.sub("CC\d->",f"CC{i}->",center_columns[i][0])
        center_columns[i][0]=re.sub("CC\d\d->",f"CC{i}->",center_columns[i][0])
        print(center_columns[i])    
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
        print(listfin[i])  
    
    #print(listfin[1],"jhgfhgfhg")    
    dict_to_insert_later={"demo":"BLUEALGO"}    
    for iii in range(len(listfin)):
        new_line=[]
        for i in range(len(listfin[iii])-1):
            if(abs(listfin[iii][i][0][1][0]-listfin[iii][i+1][0][0][0])>50):
               #print(listfin[iii][i][0][1][0],listfin[iii][i+1][0][0][0])
               new_line=listfin[iii][i+1:]
               listfin[iii]=listfin[iii][0:i+1]
               dict_to_insert_later.update({iii+1:new_line})
               break
    #print(len(listfin),"THIS IS LENGTH BEFORE ADDING ELEMENTS")
    del dict_to_insert_later["demo"]
    for i in dict_to_insert_later:
        
        print(i,dict_to_insert_later[i],"SEE ME ")
        listfin.insert(i,dict_to_insert_later[i])
        #print(dict_to_insert_later[i],listfin[i],"COMPARING HERE ")          
    #print(len(listfin),"THIS IS LENGTH AFTER ADDING ELEMENTS")
     
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
            #print(x,"THIS IS J s value in  x")
            #print(abs(listfin[x][0][0][0][0]-listfin[j][0][0][0][0]))
            if(abs(listfin[x][0][0][0][0]-listfin[j][0][0][0][0])<30 and listfin[j] not in checklist):
                 collist.append(listfin[j])
                 checklist.append(listfin[j])
                 
                 
        x=x+1         
        if(len(collist)>0):    
            columnlist.update({no:collist})
            no+=1

  
    #print(columnlist,"HERE")
    #print("SADASDASDJHDFHJSFGDJKHFGJKDFHSKFHDSKHFK")
    
    x=open("file1.txt","w+")
    x.write("TOTAL COLUMNS ->"+str(len(columnlist.keys()))+"\n")
    lolalist=[]
    print(columnlist.keys())
    for i in  columnlist.keys():
        
        #print(len(columnlist[i]))
        stringer=''
        for j in range(len(columnlist[i])):
         
         for k in range(len(columnlist[i][j])): 
         #print(j,"SEE ME SOON \n")
         #x.write(str(i)+"->"+str(columnlist[i][0][0][1]["t_"])+" -> "+" NO OF WORDS IN THIS column -> "+str(len(columnlist[i]))+"\n")    
         #print(columnlist[i][0][j][1]["t_"])
          
      
           stringer=stringer+" "+columnlist[i][j][k][1]["t_"]
        
        lolalist.append(stringer)  
        #x.write("COLUMN----------------------------------------\n"+stringer+"\n\n\n") 
    for i in range(len(lolalist)):
        
        x.write("COLUMN--------------------------------\n\n"+lolalist[i]+"\n--------------------------------\n")    
    x.close()
    for i in columnlist:
        #print(columnlist[i])
        pass
def lineswithcol(image_path,listfin):
    img=cv2.imread("image_jukebox/"+image_path)
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
            #print(valu)
            if(len(re.findall(valu,str(listfin))))<2:
                       listfin[i][j][len(listfin[i][j])-2]=000
                                



    print(f"TOTAL NO OF LINES ::::: {len(listfin)}")
    for i in range(len(listfin)):
        print("LINE NO "+str(i+1)+" ->\n")      
        for j in listfin[i]:
         #print(len(j),end="\n")
         #print("LINE NO "+str(i+1)+str({"x1,x2":(j[0][0][0],j[0][1][0]),"pos":j[3],"word":j[1]["t_"],"type":j[2],"alignment":j[4]})) 
         print(j[1]["t_"],end=" ")
        print("\r")     
    return listfin                 
def maketemplate(list_fin):
   uriidentifier=[]
   for i in range(len(list_fin)):
       stro=''
       for j in range(len(listfin[i])):
           print(listfin[i][j][1]["t_"],end=" ")
           stro=stro+listfin[i][j][1]["t_"]+" "
       uriidentifier.append(stro)
       print("\n")
   f=open("uri_final.txt","r+")
   x=f.read()
   
   x=x.split(",")
   for i in range(len(uriidentifier)):
       for word in x:
           
           if(uriidentifier[i].lower().replace("\"","").find(word.lower())>-1):
               print("FOUND")
               list_fin[i].insert(0,{"uri":"ba_"+word.replace(" ","_")})
   x=open("txt_templates/"+image_path.replace(".jpg",".txt"),"w+")

   for i in range(len(list_fin)):
       if(type(list_fin[i][0])==dict): 
         if(type(list_fin[i][1])==dict and list_fin[i][1]["uri"]=="ba_fathers_name"):  
           print(list_fin[i][1],end=" ")
           x.write(str(list_fin[i][1])+" ") 
           list_temp=list_fin[i][2:]
         else:
             print(list_fin[i][0],end=" ")
             x.write(str(list_fin[i][0])+" ") 
             list_temp=list_fin[i][1:] 
       else:
           list_temp=listfin[i]  
       if(type(list_temp[0])==dict):
           print(list_temp[0],end=" ")
           x.write(str(list_temp[0])+" ")
           list_temp=list_temp[1:]      
       for j in range(len(list_temp)):
           
           if(list_temp[j][2]["type"]=="ALPHANUMERIC" and len(list_temp[j][1]["t_"])==10 and bool(re.search("\w\w\w\w\w\d\d\d\d\w",list_temp[j][1]["t_"]))==True):
               print({"uri":"ba_pan_no"},end=" ")
               x.write(str({"uri":"ba_pan_no"})+" ")
           try:    
            if(list_temp[j][2]["type"]=="DIGIT" and len(list_temp[j][1]["t_"])==4 and list_temp[j+1][2]["type"]=="DIGIT" and len(list_temp[j+1][1]["t_"])==4 and list_temp[j+2][2]["type"]=="DIGIT" and len(list_temp[j+2][1]["t_"])==4 and len(list_temp)-1==j+2):
               x.write(str({"uri":"aadhar_no"})+" ")
               #print("AADHAR NO IS ::::: ",list_temp[j][1]["t_"],list_temp[j+1][1]["t_"],list_temp[j+2][1]["t_"])
           except:
               pass         
           print(list_temp[j][2]["type"],"length=",len(list_temp[j][1]["t_"]),end=" ")
           x.write(list_temp[j][2]["type"]+" ")    
       print("\r")
       x.write("\n")           
   x.close()         
          

for images in os.listdir("image_jukebox"):
    image_path=images
    word_list_sorted=retsortedwords(image_path)
    fina_list=columnar_new(word_list_sorted)
    listfin=linemaker(word_list_sorted)
    list_fin=lineswithcol(image_path,listfin)
    maketemplate(list_fin)
#columnmaker(listfin)
