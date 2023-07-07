import cv2
from google.cloud import vision
import os
import re
import logging
from flask import Flask,request,render_template
from fileinput import filename
import requests
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.DEBUG, filename="hello.log")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'chetan.json'
app=Flask(__name__)
@app.route('/test', methods=['GET', 'POST'])
def photoupd():
    if (request.method == "POST"):
        image_path = request.files["upd"]
        image_path.save(image_path.filename)
        return(image_path.filename)    
    return render_template("input.html")
@app.route('/test/results',methods=['GET', 'POST'])
def mainfunc():
    def get_word_bounding_vertices(image_path):
        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        # Reads the image file
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
            vertices = [(vertex.x, vertex.y)
                        for vertex in annotation.bounding_poly.vertices]
            word_bounding_vertices.append((vertices, annotation1))

        # Sorts the word bounding vertices line-wise based on Y-coordinate
        # word_bounding_vertices = sorted(word_bounding_vertices, key=lambda vertices: vertices[0][1])

        return word_bounding_vertices


    # Provide the path to your image file
    image_path = photoupd()


    line_wise_vertices = get_word_bounding_vertices(image_path)

    # Print the word bounding vertices line-wise
    i = 0
    listfin = []

    while i < len(line_wise_vertices):
        x = line_wise_vertices[i][0][0][1]
        list1 = []

        for j in range(i, len(line_wise_vertices)):
            if line_wise_vertices[j][0][0][1]-x>=-2 and line_wise_vertices[j][0][0][1]-x<=1:
                list1.append({"desc":line_wise_vertices[j][1],"vertices":line_wise_vertices[j][0]})
                
            else:
                break
            i = j + 1 
        listfin.append(list1)
    length=len(listfin)-1
    print(length+1," THIS IS STR LENGTH")
    while length>-1:
        
        if(listfin[length][0]["desc"]=='' or len(listfin[length][0]["desc"])<2):
            listfin.pop(length)
        length=length-1
    print(len(listfin)," THIS IS LENGTH AFTER TRIMMING")            
    linelist=[]
    for ii in range(len(listfin)):
        line_words=len(listfin[ii])
        x1,y1=listfin[ii][0]["vertices"][0]
        x2,y2=listfin[ii][len(listfin[ii])-1]["vertices"][1]
        linelist.append([y1,x1," x1:"+str(x1)+" x2:"+str(x2)+" y1:"+str(y1)+" y2:"+str(y2)])
        linelisttemp=[]
        for i in range(len(listfin[ii])):
            linelisttemp.append(listfin[ii][i]["desc"])
        linelist.append(linelisttemp)
    linelistfinal=[]
    for i in range(0,len(linelist),2):
        linelistfinal.append(linelist[i]+linelist[i+1])
    linelistfinal.sort(key=lambda x: x[0])
    for i in range(len(linelistfinal)):
        linelistfinal[i]=linelistfinal[i][3:]
        print(linelistfinal[i])
    return(linelistfinal)
if __name__ == "__main__":
    app.run()