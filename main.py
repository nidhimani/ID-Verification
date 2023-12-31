# pip install azure-identity
# pip install azure-cognitiveservices-formrecognizer
# pip install azure-ai-formrecognizer
# pip install mysql-connector-python
import os
import json
import cv2 as cv
import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from Scripts import sql as data
from Scripts import Formrecognizer as fr
import ultralytics
from roboflow import Roboflow
import torch
import streamlit


# rf = Roboflow(api_key="iNsqDOkc7xvm9CuNGJv7")
# project = rf.workspace("project-epimx").project("id-bdbwr")
# dataset = project.version(2).download("yolov8")

st.title("Document Verification")

# Create a file upload widget
uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    # Specify the folder where you want to save the uploaded file
    save_folder = "Data"

    # Create the folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Get the file name and extension
    file_name = uploaded_file.name

    # Define the file path to save the uploaded file
    file_path = os.path.join(save_folder, file_name)

    # Save the uploaded file to the specified folder
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    doc = file_path

    # model = ultralytics.YOLO("yolov8n.pt")

    # model.train(data = "id-2\data.yaml", epochs = 25)

    model = ultralytics.YOLO(r"runs\detect\train3\weights\last.pt")
    img = cv.imread(file_path)
    results = model(img)

    if len(results[0].boxes.cls) >= 4:
        st.write(len(results[0].boxes.cls))
        st.success("Document verified successfully")
        # Load Form Recognizer credentials from config.json
        with open("Scripts\config.json", "r") as file:
            credentials = json.load(file)
            endpoint = credentials["End_Point"]
            key = credentials["key"]

        # Connect to SQL database and retrieve documents for verification
        lis = data.sql_connection()

        # Perform document analysis using Azure Form Recognizer
        dic = fr.identify(key, endpoint, file_path)

        # image = Image.open(doc)
        # img = cv.imread(doc)
        
        
        def rescale(frame, scale = 0.5):
            width = int(frame.shape[1] * scale)
            height = int(frame.shape[0] * scale)
            dimensions = (width, height)
            # return cv.resize(frame, dimensions, interpolation = cv.INTER_LINEAR)
            return cv.resize(frame, dimensions)
        resize_img = rescale(img)
        st.image(resize_img, caption = "PLEASE CROSS-CHECK YOUR ID PROOF")
        


        # Initialize the session state for each field in dic
        for i in dic.keys():
            if i not in st.session_state:
                st.session_state[i] = ""
        # Set the default value of the text input based on session state
        st.sidebar.title("FORM")

        with st.sidebar:
            for i in dic.keys():
                text_input = st.text_input(f" {i}", st.session_state[i])


        # Function to add values to the session state
        def add():
            if dic["Document Number"] in lis:
                for key, value in dic.items():
                    if st.session_state[key] == "" and value:
                        st.session_state[key] = value  # Update 'text' session state
                    else:
                        st.session_state[key] = "None"
        verify_button = st.button("Verify Documents", on_click=add, key="add_one")

        if verify_button:
            if dic["Document Number"] in lis:
                st.success("Documents Verified")
        else:
                st.error("Please upload Valid ID")
    else:
        st.error("Please scan a valid ID")










