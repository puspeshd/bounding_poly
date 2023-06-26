import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='chetan.json'
from google.cloud import vision
import re

vision_client = vision.ImageAnnotatorClient()



def get_ocr(content):
	image = vision.Image(content=content)
	response = vision_client.document_text_detection(image=image)
	linebyline=dict()	
	#print(response.text_annotations[0].description.encode("utf-8"))

	#(response.text_annotations[0].bounding_poly.vertices)
	#response.text_annotations.pop(0)
	temp= response.full_text_annotation.pages
	#temp=temp.blocks
	#temp=temp.paragraphs
	#temp=temp.words

	for i in response.text_annotations:
		txt= i.description
		#txt=txt.encode('utf-8')
		txt=str(txt)
		
		
		bp=i.bounding_poly.vertices
		bp=list(bp)
		
		bstr=str(bp[0])
		
		bstr=bstr[bstr.find('y:')+2:]
		bstr=int(bstr)
		txt=txt.encode('utf-8')
		txt=str(txt)
		'''txt = txt.replace("\\", "")
		txt = txt.replace("|", "")
		txt = txt.replace("/", " ")
		txt = txt.replace("'\*", " ")
		txt = txt.replace("'", "")
		txt = txt.replace("\n", " ")
		txt = re.sub("x..", "", txt)
		txt = txt.replace("(","")
		txt = txt.replace(")","")
		'''
		dict1={bstr:txt}
		linebyline.update(dict1)
		for i in linebyline.keys():
			if(linebyline[i].find('b')==0):
				linebyline[i]=linebyline[i].replace("b","")
		
	#print(linebyline)
	fulllist=[]	
	listkeys=linebyline.keys()
	listkeys=sorted(listkeys)
	print(listkeys)
	
	
	templist = [linebyline[listkeys[0]]]

	for i in range(len(listkeys) - 1):
		if listkeys[i + 1] - listkeys[i] < 2:
			templist.append(linebyline[listkeys[i + 1]])
		else:
			fulllist.append(templist)
			templist = [linebyline[listkeys[i + 1]]]

	fulllist.append(templist)
			
	for i in fulllist:
	 print(i)					    
	
content=open("newaadharfortest.jpg","rb")
content=content.read()
get_ocr(content)