import streamlit as st
import json
import requests
import base64
from PIL import Image
import io
#import tkinter as tk
from streamlit_pdf_viewer import pdf_viewer
#import turtle



#these are main classes your image is trained on
#you can define the classes in alphabectical order
PREDICTED_LABELS = ["astilbe", "bellflower","carnation"]  # Edit 1
PREDICTED_LABELS.sort()

def get_prediction(image_data):
  #replace your image classification ai service URL
  url = 'https://askai.aiclub.world/cba6cd94-0266-4d65-ab09-75b46e2dd069'  #Edit 2-- get endpoint URL from navigator by deploying your onnx model
  r = requests.post(url, data=image_data)
  response = r.json()['predicted_label']
  score = r.json()['score']
  #print("Predicted_label: {} and confidence_score: {}".format(response,score))
  return response, score


#setting up the title
st.markdown("""
<style>
body {
    background-color: #00ff00;
}
</style>
""", unsafe_allow_html=True)
st.title("Welcome to Flower Image Classifier Web App!")#change according to your project   #edit 3

#root=tk.Tk()
#root.config(bg='light blue')
#root.geometry(400,400)
#root.title("Flower Image Classifier")
#root.mainloop()
#turtle.Screen().bgcolor(0,0,255)

#creating the tabs for the web app

tab1, tab2 = st.tabs(["Make Prediction", "View Report"])

with tab1:
  #setting up the title
  st.header("Flowers Image Classifier")#change according to your project   #Edit 3
  #setting up the subheader
  st.subheader("File Uploader")#change according to your project

  #file uploader
  image = st.file_uploader(label="Upload any flower image of(astilbe,bellflower,carnation) ",accept_multiple_files=False, help="Upload an image to classify them")
  if image:
    #converting the image to bytes
    img = Image.open(image)
    buf = io.BytesIO()
    img.save(buf,format = 'JPEG')
    byte_im = buf.getvalue()

    #converting bytes to b64encoding
    payload = base64.b64encode(byte_im)

    #file details
    file_details = {
      "file name": image.name,
      "file type": image.type,
      "file size": image.size
    }

    #write file details
    st.write(file_details)

    #setting up the image
    st.image(img)

    #predictions
    response, scores = get_prediction(payload)

    #if you are using the model deployment in navigator
    #you need to define the labels
    response_label = PREDICTED_LABELS[response]

    col1, col2 = st.columns(2)
    with col1:
      st.metric("Prediction Label",response_label)
    with col2:
      st.metric("Confidence Score", max(scores))




with tab2:

  # Title of the app
  st.header("My Report")

  #add github link
  #st.link_button("My Github Repository", "URL of your guthub repo") #syntax

  st.link_button("My Github Repository", "https://github.com/arunamikkili/Flower_Demo") #Edit 4https://github.com/arunamikkili/Flower_Demo

  # URL of the PDF file in the GitHub repository
  # sample url -> "https://raw.githubusercontent.com/yourusername/yourrepository/branch/yourfile.pdf"
  # https://github.com/arunamikkili/Flower_Demo/blob/main/sample.pdf
  pdf_url = "https://raw.githubusercontent.com/arunamikkili/Flower_Demo/main/sample.pdf"

  # Fetch the PDF file from GitHub
  response = requests.get(pdf_url)

  # Check if the request was successful
  if response.status_code == 200:
    # Display the PDF in the Streamlit app
    st.download_button(label="Download Report", data=response.content, file_name="downloaded.pdf")
    if st.button("Show Report"):
        with st.sidebar:
            pdf_viewer(response.content)

  else:
    st.error("Failed to fetch PDF file. Please check the URL.")


