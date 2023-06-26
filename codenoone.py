from google.cloud import vision
import os
import re
import logging
logging.basicConfig(level=logging.DEBUG, filename="hello.log")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'chetan.json'


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
    desc = annotations[1:]
    
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
image_path = 'newaadharfortest.jpg'

line_wise_vertices = get_word_bounding_vertices(image_path)

# Print the word bounding vertices line-wise
i = 0
listfin = []

while i<len(line_wise_vertices):
    strtemp=''
    strtemp=strtemp+line_wise_vertices[i][1]
    if(line_wise_vertices[i][0][0][1]==line_wise_vertices[i+1][0][0][1]):
        strtemp=strtemp+line_wise_vertices[i+1][1]
        listfin.append(str(line_wise_vertices[i][0])+" "+strtemp+"\n")
        i=i+2
        continue
    i=i+1
logging.info(f"{listfin}")    
print(listfin)        