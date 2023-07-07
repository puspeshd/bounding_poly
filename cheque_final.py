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
logging.basicConfig(level=logging.DEBUG, filename="hello.log")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'chetan.json'
app=Flask(__name__)
CORS(app)
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
        x1,y1=listfin[ii][0]["vertices"][1]
        x2,y2=listfin[ii][len(listfin[ii])-1]["vertices"][2]
        linelist.append([y2,x1," x1:"+str(x1)+" x2:"+str(x2)+" y1:"+str(y1)+" y2:"+str(y2)])
        linelisttemp=[]
        for i in range(len(listfin[ii])):
            linelisttemp.append(listfin[ii][i]["desc"])
        linelist.append(linelisttemp)
    linelistfinal=[]
    for i in range(0,len(linelist),2):
        linelistfinal.append(linelist[i]+linelist[i+1])
    linelistfinal.sort(key=lambda x: x[0])
    fullnfinal=[]
    i=0
    while i<(len(linelistfinal)):
        finindex=i
        tempo=[linelistfinal[i]]
        for j in range(i+1,len(linelistfinal)):
            if(linelistfinal[j][0]-linelistfinal[i][0]<=20):
                tempo.append(linelistfinal[j])
                finindex=j
        fullnfinal.append(tempo)        
        i=finindex+1
    for i in fullnfinal:
        i.sort(key=lambda x: x[1])
        for j in range(len(i)):
            #i[j]=i[j][:]
            pass
            
    
    img=cv2.imread(image_path)
    h,w,_=img.shape
    print(h,w)    
    leftlist=[]
    rightlist=[]
    centerlist=[]
    for i in range(len(fullnfinal)):
        if(fullnfinal[i][0][1]<=w//2):
            leftlist.append(fullnfinal[i])
        
        elif(fullnfinal[i][0][1]>=w//2):
            rightlist.append(fullnfinal[i])
            
    
    for i in range(len(leftlist)):
        for j in range(len(leftlist[i])):
            leftlist[i][j]=leftlist[i][j][3:]
        #print(leftlist[i])
        
    
        
    for i in range(len(rightlist)):
        for j in range(len(rightlist[i])):
            rightlist[i][j]=rightlist[i][j][3:]                     
    
        #print(rightlist[i])
    print("---------------------------------------LEFT-------------------------------------------")    
    for i in range(len(leftlist)):
         leftlist[i]=str(leftlist[i])
         leftlist[i]=leftlist[i].replace("[","")
         leftlist[i]=leftlist[i].replace(']',"")
         leftlist[i]=leftlist[i].replace(',','')
         leftlist[i]=leftlist[i].replace('-','')
         leftlist[i]=leftlist[i].replace('.','')
         leftlist[i]=leftlist[i].replace('-','')
         leftlist[i]=leftlist[i].replace("'",'')
         print(leftlist[i])    
    
    

    print("---------------------------------------RIGHT-------------------------------------------")

    for i in range(len(rightlist)):
         rightlist[i]=str(rightlist[i])
         rightlist[i]=rightlist[i].replace("[","")
         rightlist[i]=rightlist[i].replace(']',"")
         rightlist[i]=rightlist[i].replace(',','')
         rightlist[i]=rightlist[i].replace('-','')
         rightlist[i]=rightlist[i].replace('.','')
         rightlist[i]=rightlist[i].replace('-','')
         rightlist[i]=rightlist[i].replace("'",'')
         print(rightlist[i])    



    os.remove(image_path)           
    micr=''
    cheque_no=''
    date=''
    amount_n=''
    amount_w=''
    payee='' 
    try:
        micr=fullnfinal[len(fullnfinal)-1]
        
    except:
        pass
    try:
       try: 
        date=str(rightlist[0:3]).replace(" ",'')
        spano=re.search("\d\d\d\d\d\d\d\d", date).span()
        date=date[spano[0]:spano[1]]
       except:
         date=str(leftlist[0:3]).replace(" ",'')
         spano=re.search("\d\d\d\d\d\d\d\d", date).span()
         date=date[spano[0]:spano[1]]   
    except:
        date="DATE CANT BE FOUND "
    try:
        micr=leftlist[len(leftlist)-1]
        micr=micr.replace(" ","")
        micr=micr.replace("*",'')
        micr=micr.replace("O",'0')
        print(micr)
        if(micr[0:20].isdigit()):
            cheque_no=micr[0:6]
            micr=micr[6:15]
            print("if loop",micr)
        else:
            print("ELSE LOOP")
            micr=rightlist[len(rightlist)-1]
            micr=micr.replace(" ","")
            micr=micr.replace("*",'')
            micr=micr.replace("O",'0')
            spano=re.search("\d\d\d\d\d\d",micr).span()
            cheque_no=micr[spano[0]:spano[1]+1]
            micr=micr[spano[1]+1:] 
              
        
        try:   
           spano=re.search("\d\d\d\d\d\d\d\d\d",micr).span()
           micr= micr[spano[0]:spano[1]+1]   
        except:
            micr="NOT ABLE TO FIND MICR"
        if(cheque_no.isdigit()==False):
            cheque_no="NOT ABLE TO FIND CHEQUE NO"    
        
        
    except:
        cheque_no='SOME PROBLEM'
        micr='SOME PROBLEM'
    
    try:
        for i in range(len(leftlist)):
            key1=leftlist[i].lower().find("pay ")
            key2=leftlist[i].lower().find("pat ")
            if(key1>-1 or key2>-1 ):
                if(key1>key2):
                    payee=leftlist[i][key1+3:]
                elif(key1<key2):
                    payee=leftlist[i][key2+3:]
                elif(key1==key2) and key1==-1:
                    payee="BLANK>>>>>>FIND NEW LOGIC" 
                else:
                    payee="SOME PROB" 
                break              
    except:
        payee="?????" 
    try:
       for i in range(len(leftlist)):
            key1=leftlist[i].lower().find("rupees ")
            key2=leftlist[i].lower().find(" only")
            print(key1,key2)
            if(key1==-1 or key2 == -1):
                amount_w = " can't found"
            else:
                amount_w=leftlist[i][key1+6:key2]    
                break
            
    except:
         amount_w="NOT FOUND "
    try:
        amount_n=words2num.w2n(amount_w)
    except:
        amount_n='343432'         
    def canvasdata(micr):

        micr_code =micr
        #print(type(micr_code),micr_code)
                 
        url = f"https://micr.bankifsccode.com/{str(micr_code)}"
            #for i in range(1, 11):
        
            
            #proxy = next(proxyPool)
            #time.sleep(2)
        response = requests.get(url)
        soup=BeautifulSoup(response.content,'html.parser')
            #print(soup)
            
            #print(response.text)
        str1=soup.text
        
        if(str1.find("MICR Code:-")>-1):
                str1=str1[str1.find("MICR Code:-")+21:]
        
            #print(str1)
            
        if(str1.find("MICR Code:")>-1):
                str1=str1[:str1.find("MICR Code:")]
            #print(str1)
        str1=str1.replace("IFSC Code: ","@@@")
        ifsc=str1[str1.find("@@@")+3:str1.find("@@@")+14]
        str1=re.sub(r"[^a-zA-Z0-9 ]", "", str1)
        return([ifsc,str1])
    ifsc,add=canvasdata(micr)
    add=add.replace("Bank","\nBank : ")
    add=add.replace("Address","\nAddress : ")
    add=add.replace("State","\nState : ")
    add=add.replace("District","\nDistrict : ")
    add=add[:add.find("Click here for")]
    add=add.split("\n")
    findic={"date":date,"payee":payee,"amount_w":amount_w,"amount_n":amount_n,"micr":micr,"chq_no":cheque_no,"ifsc":ifsc,"address":add}
    return (findic)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")