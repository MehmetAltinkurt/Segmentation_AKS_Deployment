import io
import os
import cv2 as cv
import requests
import PIL
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import numpy as np

import streamlit as st

# interact with FastAPI endpoint
#backend = "http://192.168.1.25:8000/segmentation" #"http://127.0.0.1:8000/segmentation" #"http://fastapi:8000/segmentation"
 #os.getenv("server_URL")+"/segmentation" #"https://7853-176-233-25-85.ngrok-free.app/segmentation"#"http://"+os.getenv("FASTAPI_SERVICE_SERVICE_HOST")+":"+os.getenv("FASTAPI_SERVICE_SERVICE_PORT")+"/segmentation"

backend = "http://"+os.getenv("FASTAPI_SERVICE_SERVICE_HOST")+":"+os.getenv("FASTAPI_SERVICE_SERVICE_PORT")+"/segmentation"
def process(image, server_url: str):

    m = MultipartEncoder(fields={"file": ("filename", image, "image/jpeg")})

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000, stream=True
    )

    return r


# construct UI layout
st.title("DeepLabV3 image segmentation")

st.write(
    """Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
         This streamlit example uses a FastAPI service as backend.
         Visit this URL at `:8000/docs` for FastAPI documentation."""
)  # description and instructions

input_image = st.file_uploader("insert image")  # image upload widget

if st.button("Get segmentation map"):

    col1, col2 = st.columns(2)

    if input_image:
        segments = process(input_image, backend)
        original_image = Image.open(input_image).convert("RGB")
        
        img_stream = io.BytesIO(segments.content)  
        segmented_image = cv.imdecode(np.frombuffer(img_stream.read(), np.uint8), cv.IMREAD_UNCHANGED)      
        segmented_image=segmented_image[:, :, ::-1]

        col1.header("Original")
        col1.image(original_image, use_column_width=True)
        col2.header("Segmented")
        col2.image(segmented_image, use_column_width=True)#, channels="BGR")

    else:
        # handle case with no image
        st.write("Insert an image!")
