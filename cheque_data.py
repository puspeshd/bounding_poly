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
    for i in linelistfinal:
        print(i)

    img=cv2.imread(image_path)
    h,w,_=img.shape
    print(h,w)    
    leftlist=[]
    rightlist=[]
    centerlist=[]
    for i in range(len(linelistfinal)):
        if(linelistfinal[i][1]<=w//3):
            leftlist.append(linelistfinal[i])
        elif(linelistfinal[i][1] >= w//3 and linelistfinal[i][1]<=w//3+w//3):
            centerlist.append(linelistfinal[i])
        elif(linelistfinal[i][1]>=w//3+w//3):
            rightlist.append(linelistfinal[i])
            
    columnar=[]
    used_fields=[]
    for i in range(len(leftlist)):
        list1 = []
        if(leftlist[i][3:] not in used_fields):
            list1.append(leftlist[i][3:])
            used_fields.append(leftlist[i][3:])
        
        
        for j in range(i, len(leftlist)):
            if leftlist[j][1]-leftlist[i][1]<=1 and leftlist[j][1]+leftlist[i][1]>=0 :
             if(leftlist[j][3:] not in used_fields ): 
                list1.append(leftlist[j][3:])
                used_fields.append(leftlist[j][3:])
                last_index=j
            
        i=last_index     
        if(len(list1)>0):   
            columnar.append(list1)

    columnar1=[]
    used_fields1=[]
    for i in range(len(rightlist)):
        list1 = []
        if(rightlist[i][3:] not in used_fields1):
            list1.append(rightlist[i][3:])
            used_fields1.append(rightlist[i][3:])
        
        
        for j in range(i, len(rightlist)):
            if rightlist[j][1]-rightlist[i][1]<=1 and rightlist[j][1]+rightlist[i][1]>=0 :
             if(rightlist[j][3:] not in used_fields1 ): 
                list1.append(rightlist[j][3:])
                used_fields1.append(rightlist[j][3:])
                last_index=j
            
        i=last_index     
        if(len(list1)>0):   
            columnar1.append(list1)  
    columnar2=[]
    used_fields2=[]
    for i in range(len(centerlist)):
        list1 = []
        if(centerlist[i][3:] not in used_fields2):
            list1.append(centerlist[i][3:])
            used_fields2.append(centerlist[i][3:])
        
        
        for j in range(i, len(centerlist)):
            if centerlist[j][1]-centerlist[i][1]<=1 and centerlist[j][1]+centerlist[i][1]>=0 :
             if(centerlist[j][3:] not in used_fields2 ): 
                list1.append(centerlist[j][3:])
                used_fields2.append(centerlist[j][3:])
                last_index=j
            
        i=last_index  
        if(len(list1)>0):   
            columnar2.append(list1)

    print("_____________________________________-----------------------LEFT------------________________________")
    for colu in range(len(columnar)):
        
        print("column no ",colu,"::::",columnar[colu])
    print("_____________________________________-----------------------RIGHT------------________________________")    
    for colu1 in range(len(columnar1)):
        print("column no ",colu1,"::::",columnar1[colu1])  
    print("_____________________________________-----------------------CENTER------------________________________")    
    for colu2 in range(len(columnar2)):
        print("column no ",colu2,"::::",columnar2[colu2])  
    print("****************************************************************************.................")    
    try:
        date=str(columnar1[0])
        date=date.replace(" ","")
        date=date.replace("[","")
        date=date.replace(']',"")
        date=date.replace(',','')
        date=date.replace('-','')
        date=date.replace('.','')
        date=date.replace('-','')
        date=date.replace("'",'')
        #print(date,"----------------")
        date1=re.search("\d\d\d\d\d\d\d\d",date).span()
        date=date[date1[0]:date1[1]]
    except:
        date=''   
    try:
            tempstr=str(columnar[0])
            if(bool(re.search("pay\W",tempstr.lower()))==True):
                print("FOUND PAY EARLIER")
                spano=re.search("pay\W",tempstr.lower()).end()
                payee=tempstr[spano+1:]
            elif(bool(re.search("pat\W",tempstr.lower()))==True):
                print("FOUND PAY EARasdLIER")
                spano=re.search("pat\W",tempstr.lower()).end()
                payee=tempstr[spano+1:]
            payee=payee.replace("[","")
            payee=payee.replace(']',"")
            payee=payee.replace(',','')
            payee=payee.replace('-','')
            payee=payee.replace('.','')
            payee=payee.replace('-','')
            payee=payee.replace("'",'')
            payee=payee.lower().replace("pay",'')
            payee=payee.title()
            for i in range(len(payee)):
                if(payee[i].isnumeric()==True):
                    payee=payee[0:i]
                    break
            spano=payee.lower().find("rupees")
            if(spano>-1):
                payee=payee[0:spano]    

            print(payee)


    except exception as e:
        payee=''
        print(e)
    try:        
     strt=str(columnar[0]).lower().find("rupees")
     
     amount_w=str(columnar[0])[strt+6:]
     end=amount_w.lower().find("only")
     amount_w=amount_w[0:end]
     amount_w=amount_w.replace("[","")
     amount_w=amount_w.replace(']',"")
     amount_w=amount_w.replace(',','')
     amount_w=amount_w.replace('-','')
     amount_w=amount_w.replace('.','')
     amount_w=amount_w.replace('-','')
     amount_w=amount_w.replace("'",'')
     for i in range(len(amount_w)):
         if(amount_w[i].isdigit()==True):
             amount_w=amount_w[0:i]
             break
    except:
        amount_w=''
    try:     
        amount_no=str(columnar1[1])
        amount_n=''
        for i in range(len(amount_no)):
            if(amount_no[i].isdigit()==True):
                amount_n=amount_n+amount_no[i]
    except:
        amount_n=["Not found with this logic"]
    try:        
     
     micro=str(columnar[len(columnar)-1])
     micro=re.sub(r"[\[\]\,\s\'*]",'',micro)
     print(micro)
     if(micro.isalpha()==True):
         micro=str(columnar[len(columnar)-2])
         micro=re.sub(r"[\[\]\,\s\'*]",'',micro)
     micr=''
     if(micro.lower().find("prefix")>-1):
         print("THIS LOOP IS ON ")
         indo=micro.lower().find("prefix")
         print(indo)
         
         micro=micro[indo+17:]
         print(micro)
     for i in range(len(micro)):
         if(micro[i].isnumeric()==True or micro[i]==('O')):
             micr=micr+micro[i]
     micr=micr.replace('O','0')         
     chq_no=micr[0:6]
     if(micr[6:7]=='1'):
         micr=micr[7:16]
     else:
         micr=micr[6:15]    
         
    

    except:
        micr=''
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
                str1=str1[str1.find("MICR Code:-")+1:]
            #print(str1)
        if(str1.find("MICR Code:")>-1):
                str1=str1[:str1.find("MICR Code:")]
            #print(str1)
        str1=str1.replace("IFSC Code: ","@@@")
        ifsc=str1[str1.find("@@@")+3:str1.find("@@@")+14]
        return([ifsc,str1])
                
    findic={"date":date,"payee":payee,"amount_w":amount_w,"amount_n":amount_n,"micr":micr,"chq_no":chq_no,"ifsc_code":canvasdata(micr)[0],"comments":canvasdata(micr)[1]}
    print(findic) 
    os.remove(image_path)
    return (findic)
if __name__=='__main__':
    app.run()