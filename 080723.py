
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
from openpyxl import Workbook,load_workbook
from openpyxl.utils import get_column_letter
import pandas as pd
from copy import copy
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'chetan.json'
client = vision.ImageAnnotatorClient()
image_path="cheque1.png"
def retsortedwords(image_path):
    with open(image_path, 'rb') as image_file:
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
         
        if(annotation1.replace(' ','').isalpha()):
           type="ALPHA "
        elif(annotation1.replace(' ','').isdigit()):
            type="DIGIT "
        elif(annotation1.replace(' ','').isalnum()):
            type="ALPHANUMERIC" 
        elif(len(annotation1.replace(' ',''))<1):
            type="NULL"
        else:
            type="SPECIAL CHARACTER/S "           
        vertices = [(vertex.x, vertex.y)
                    for vertex in annotation.bounding_poly.vertices]
        word_bounding_vertices.append((vertices,{"t_": annotation1},{"length":len(annotation1),"type":type}))
    word_bounding_vertices = sorted(word_bounding_vertices, key= lambda x: x[0][0][1])
    for waka in word_bounding_vertices:
            print(waka)
    return word_bounding_vertices    
word_list_sorted=retsortedwords(image_path)            
def linemaker(word_list_sorted):
    i = 0
    listfin = []

    while i < len(word_list_sorted):
        x = word_list_sorted[i][0][0][1]
        list1 = []

        for j in range(i, len(word_list_sorted)):
            if word_list_sorted[j][0][0][1]-x>=-2 and word_list_sorted[j][0][0][1]-x<=10:
                list1.append(word_list_sorted[j])
                
            else:
                break
            i = j + 1 
        listfin.append(list1)
    dic_to_insert_later={}    
    for iii in range(len(listfin)):
        new_line=[]
        for i in range(len(listfin[iii])):
            if(abs(listfin[iii][i][0][0][0]-listfin[iii][i+1][0][1][0])>25):
               print(listfin[iii][i][0][0][0],listfin[iii][i+1][0][1][0])
               new_line=listfin[iii][i+1:]
               listfin[iii][i]=listfin[iii][i][:i+1]
               dict_to_insert_later={iii+1:new_line}
    for i in dict_to_insert_later:
        listfin.insert(i.key(),i.value())           

    
    
    
    x=open("file1.txt","w+")
    x.write("TOTAL LINES ->"+str(len(listfin))+"\n")
    for i in range(len(listfin)):
        x.write("LINE NO "+str(i+1)+" -> "+str(listfin[i])+" NO OF WORDS IN THIS LINE -> "+str(len(listfin[i]))+"\n")
        
linemaker(word_list_sorted)        