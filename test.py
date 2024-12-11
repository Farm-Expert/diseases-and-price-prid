from fastapi import FastAPI
from pydantic import BaseModel
import requests
import PIL.Image
import google.generativeai as genai

genai.configure(api_key="AIzaSyCzdI-Itcf8eSbrg8IHeNTfOhzeqkDKTg4")

def read(text):
    res=""
    for chunks in text:
        chunks.text.replace('*','')
        res=res+ chunks.text
    return res

model=genai.GenerativeModel("gemini-pro")
vision=genai.GenerativeModel("gemini-1.5-pro")

history=[]
chat= model.start_chat(history=history)

app=FastAPI()

def chatting(text):
    try:
        text=chat.send_message(text)
        return {"Success":read(text)}
    except:
        return {"Error": "Harmfull words found in chat"}

def viewmodel(text,img):
    try:
        res=vision.generate_content([text,img])
        res.resolve()
        return {"Success":read(res)}
    except:
        return {"Error": "Harmfull words found in chat"}
# crop name location crop price 


class Textmessage(BaseModel):
    CropName:str
    Location:str

class Viewmessage(BaseModel):
    imgurl:str
    # message:str


@app.get("/")
def home():
    return {"Kate": "Welcome to kate"}

@app.post("/priceprediction")
def chatAPI(message:Textmessage):
    prediction=message.CropName + message.Location
    message=f"I will provide you crop name and location {prediction} as input please provide the price of the crop at that location. Give some suggestive crops which have best price for that location and suggest me higer price loactions for that particular crop in India. respond in json format with keys as crop_name, price, location, suggested_crops, locations_with_higher_prices. example "
    message= message+'{"crop_name": "strawberry", "location": "Gwalior", "locations_with_higher_prices": [{"location": "Mumbai", "price": "140 per kg"}, {"location": "Delhi", "price": "120 per kg"}], "price": "100 per kg", "suggested_crops": ["banana", "papaya", "guava"]}'
    return chatting(message)

@app.post("/vision")
def visionAPI(view:Viewmessage):
    imgurl=view.imgurl
    print(imgurl)
    if(len(imgurl)>6 and imgurl[:6]=="https:"):
        imgurl=requests.get(imgurl)
        image_blob = imgurl.content

        with open('image.jpg', 'wb') as f:
            f.write(image_blob)
        imgurl='image.jpg'
    imgurl = PIL.Image.open(imgurl)

    message="I will provide you an image of infected plant leaf, you have to respond in json format with success:pass and rest key value pairs as plant_name: 'cactus', disease_name: 'yellow leaves', symptoms:[], precautions:[], treatment:[]. the value for symptoms, precautions, treatment should also be a list if image is not plant leaf then print this in a json format with key as success:fail, message: this is not a plant leaf. please provide plant leaf. if it is a healthy plant, then return json with success:healthy, plant name, common_disease, message"
        
    # print(message)
    return viewmodel(message,imgurl)
