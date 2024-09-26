import sys
import os
#import time

from google.cloud import logging
from google.cloud import storage
import gradio as gr
import vertexai.generative_models

from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)

#ProjectInfo
PROJECT_ID = os.environ.get("GCP_PROJECT")  # Your Google Cloud Project ID
LOCATION = os.environ.get("GCP_REGION")  # Your Google Cloud Project Region
GCP_BUCKET=os.environ.get("GCP_BUCKET") #The Bucket were the uploaded files will be stored

# PROJECT_ID = "arctic-analyzer-435209-m1"  # @param {type:"string"}
# LOCATION = "europe-west3"  # @param {type:"string"}
vertexai.init(project=PROJECT_ID, location=LOCATION)

#Logging
client = logging.Client(project=PROJECT_ID)
client.setup_logging()
log_name = "genai-vertex-text-log"
logger = client.logger(log_name)

#MODEL
MODEL_ID = "gemini-1.5-pro"  # @param {type:"string"}
#MODEL_ID = "gemini-1.5-flash"  # @param {type:"string"}
# Load a example model without system instructions
##model = GenerativeModel(MODEL_ID)
# Load a example model with system instructions
model = GenerativeModel(
    MODEL_ID,
    system_instruction=[
        "You are a helpful assistant.",
    ],
)

############Optional#####################
# Set model parameters
generation_config = GenerationConfig(
    temperature=0.9,
    top_p=1.0,
    top_k=32,
    candidate_count=1,
    max_output_tokens=8192,
)
# Set safety settings
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
}

###TAB 1 Text Only
###Function to ask Gemini with text only prompt
def ask_gemini_text(prompt):
    logger.log_text(prompt)
    contents = [prompt]
    response = model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return response.text
#test function
#ask_gemini_text("why is the sky blue?")

###TAB 2 PDF ANALYSIS
def ask_gemini_text_and_pdf(prompt,pdf_file):
    logger.log_text(prompt)
    pdf_file_uri= upload_pdf_to_gcs(pdf_file)
    print(pdf_file_uri)
    #pdf_file_uri="gs://demo_gradio_data/test.pdf"
    pdf_file_part = Part.from_uri(pdf_file_uri, mime_type="application/pdf")
    contents = [prompt, pdf_file_part]
    response = model.generate_content(contents)
    return response.text 


def upload_pdf_to_gcs(pdf_file):
    """Uploads a PDF file to a GCS bucket.
    Args:
       pdf_file: The uploaded PDF file.
       # bucket_name: The name of the GCS bucket.
       # file_name: The desired name for the file in the bucket.
    """
    bucket_name='demo_gradio_data'
    file_name="mypdf.pdf"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
   # Open the PDF file and read its contents
    with open(pdf_file, 'rb') as f:  # Open in binary mode ('rb') for PDF files
        pdf_data = f.read()
    pdf_file_uri=f"gs://{bucket_name}/{file_name}"
    # Upload the file to GCS
    blob.upload_from_string(pdf_data, content_type='application/pdf')
    # Add a 1-second delay
    #time.sleep(3)
    return pdf_file_uri


    ######TAB 3 IMAGE

##Function to ask Gemini with text prompt and image
def ask_gemini_text_and_image(prompt,image_file):
    logger.log_text(prompt)
    image_file_uri= upload_image_to_gcs(image_file)
    print(image_file_uri)
    image_file_part = Part.from_uri(image_file_uri, mime_type='image/png')
    # ##image
    # image_file_path = "cloud-samples-data/generative-ai/image/a-man-and-a-dog.png"
    # image_file_uri = f"gs://{image_file_path}"
    # image_file_url = f"https://storage.googleapis.com/{image_file_path}"
    # IPython.display.Image(image_file_url, width=450)
    # image_file = Part.from_uri(image_file_uri, mime_type="image/png")
    contents = [prompt, image_file_part]
    response = model.generate_content(contents)
    return response.text


def upload_image_to_gcs(image_file):
    """Uploads an image file to a GCS bucket.
    Args:
       image_file: The uploaded image file.
    """
    bucket_name = 'demo_gradio_data'  # Replace with your GCS bucket name
        # Determine the content type based on the file extension
    if image_file.lower().endswith('.jpg') or image_file.lower().endswith('.jpeg'):
        content_type = 'image/jpeg'
        file_name_type='.jpg'
    elif image_file.lower().endswith('.png'):
        content_type = 'image/png'
        file_name_type='.png'
    elif image_file.lower().endswith('.gif'):
        content_type = 'image/gif'
        file_name_type='.gif'
    else:
        content_type = 'application/octet-stream'  # Default to a generic type

    file_name=f"myimage{file_name_type}"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    # Open the image file and read its contents
    with open(image_file, 'rb') as f:
        image_data = f.read()

    image_file_uri = f"gs://{bucket_name}/{file_name}"

    # Upload the file to GCS
    blob.upload_from_string(image_data, content_type='image/png')

    return image_file_uri


    ##Function to ask Gemini with text prompt and video
def ask_gemini_text_and_video(prompt,video_file):
    logger.log_text(prompt)
    video_file_uri= upload_video_to_gcs(video_file)
    print(video_file_uri)
    video_file_part = Part.from_uri(video_file_uri, mime_type='video/mp4')
    contents = [prompt, video_file_part]
    response = model.generate_content(contents)
    return response.text


def upload_video_to_gcs(video_file):
    """Uploads a video file to a GCS bucket.
    Args:
       video_file: The uploaded image file.
    """
    bucket_name = 'demo_gradio_data'  # Replace with your GCS bucket name
    # Determine the content type based on the file extension
    if video_file.lower().endswith('.mp4'):
        content_type = 'video/mp4'
        file_name_type = '.mp4'
    elif video_file.lower().endswith('.avi'):
        content_type = 'video/avi'
        file_name_type = '.avi'
    elif video_file.lower().endswith('.mov'):
        content_type = 'video/quicktime'
        file_name_type = '.mov'
    else:
        content_type = 'application/octet-stream'  # Default to a generic type

    file_name=f"myvideo{file_name_type}"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Open the video file and read its contents
    with open(video_file, 'rb') as f:
        video_data = f.read()

    video_file_uri = f"gs://{bucket_name}/{file_name}"

    # Upload the file to GCS
    blob.upload_from_string(video_data, content_type='image/png')

    return video_file_uri



    # Define the inputs for both functionalities
inputs_pdf = [
    gr.Textbox(lines=5,label="Enter prompt:", value="You are a very professional document summarization specialist. Summarize the given document."),
    gr.File(label="Upload PDF File"),
    #gr.Textbox(label="PDF File Name"),
    # ... other inputs for PDF ...
]

inputs_image = [
    gr.Textbox(lines=5, label="Enter prompt:", value="What is in the picture?"),
    gr.Image(label="Upload an Image", type="filepath"),
    #gr.Textbox(label="Image File Name"),
]

prompt_video = """
#   Look through each frame in the video carefully and answer the questions.
#   Only base your answers strictly on what information is available in the video attached.
#   Do not make up any information that is not part of the video and do not be too
#   verbose, be to the point.

#   Questions:
#   - What is happening in the video? Provide a summary.
#   - At which moment is the most important event, what is this and what is the exact timestamp?
# """
# contents = [video_file, image_file, prompt]

# response = model.generate_content(contents)
# print(response.text)


inputs_video = [
    gr.Textbox(lines=5, label="Enter prompt:", value=prompt_video),
    gr.Video(label="Upload a Video"),
    #gr.Textbox(label="Video File Name"),
]

# Create the Gradio interface with tabs
with gr.Blocks(theme=gr.themes.Default(primary_hue="orange")) as demo:
    with gr.Tab("Ask Gemini"):
        gr.Interface(
            fn=ask_gemini_text,
            inputs=[gr.Textbox(lines=5,label="Enter prompt:", value="Give me some productivity tips for my week!")],
            outputs="text",
            theme=gr.themes.Default(primary_hue="orange"),
        )

    with gr.Tab("PDF Analysis"):
        gr.Interface(
            fn=ask_gemini_text_and_pdf,
            inputs=inputs_pdf,
            outputs="text",
            theme=gr.themes.Default(primary_hue="orange"),
        )

    with gr.Tab("Image Analysis"):
        gr.Interface(
            fn=ask_gemini_text_and_image,
            inputs=inputs_image,
            outputs="text",
            theme=gr.themes.Default(primary_hue="orange"),
        )

    with gr.Tab("Video Analysis"):
        gr.Interface(
            fn=ask_gemini_text_and_video,
            inputs=inputs_video,
            outputs="text",
            theme=gr.themes.Default(primary_hue="orange"),
        )

# Launch the interface
demo.launch(server_name="0.0.0.0", server_port=8080,debug=True)