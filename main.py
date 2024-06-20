#!/usr/bin/env python
# coding: utf-8

import json
import logging
import os
import sys
import time
import requests
import streamlit as st

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="Text to Avatar Video Synthesis",
    layout="centered",  # Wide layout
    initial_sidebar_state="expanded"  # Expanded sidebar
)

# Image above the sidebar
image_path = os.path.join(os.path.dirname(__file__), 'assets/avatar.png')  # Assuming avtar.png is in the same directory as this script
logo_path = os.path.join(os.path.dirname(__file__), 'assets/logo.png')  # Assuming logo.png is in the same directory as this script
image_url = st.image(image_path, width=400)
st.sidebar.image(logo_path, caption='Avatar Image', width=100)

# CSS for styling
st.markdown(
    """
    <style>
    .st-bf {
        background-color: #f0f0f0; /* Light gray background for main content */
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Soft shadow */
    }
    .st-ei {
        background-color: #ffffff; /* White background for sidebar */
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Soft shadow */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Information Pane
st.sidebar.title("Information")
st.sidebar.markdown(
    """
    <div class="st-ei">
    <p>In order to use this service, you must have an active Azure Service. Create a service group (minimum plan is Standard. Free subscription is ok, but need to select standard - pay as you go).</p>
    <hr style="border-top: 1px solid #ddd;"> <!-- Horizontal line -->
    <p>Then only the speech service of Azure shows the dashboard with the "Text to Speech with Avatar" option.</p>
    <hr style="border-top: 1px solid #ddd;"> <!-- Horizontal line -->
    <p>Copy the key, and your region (Region must be any of the 3 - West US 2, West Europe, and Southeast Asia).</p>
    <hr style="border-top: 1px solid #ddd;"> <!-- Horizontal line -->
    <p>Then play with our platform.</p>
    <hr style="border-top: 1px solid #ddd;"> <!-- Horizontal line -->
    <p>Refer Azure Example: https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/yulin/batch-avatar/samples/batch-avatar/python/synthesis.py</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Input fields
SUBSCRIPTION_KEY = st.text_input("Enter your Speech API subscription key:", type="password")

# Predefined list of regions
regions = [
    "westus2", "westeurope", "southeastasia"
]
SERVICE_REGION = st.selectbox("Select your Speech API service region:", regions)

NAME = "Simple avatar synthesis"
DESCRIPTION = "Simple avatar synthesis description"

# The service host suffix.
SERVICE_HOST = "customvoice.api.speech.microsoft.com"


def submit_synthesis(text):
    if not (SERVICE_REGION and SUBSCRIPTION_KEY and text):
        st.error('Please fill in all required fields.')
        return
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Content-Type': 'application/json'
    }

    payload = {
        'displayName': NAME,
        'description': DESCRIPTION,
        "textType": "PlainText",
        'synthesisConfig': {
            "voice": "en-US-JennyNeural",
        },
        'inputs': [
            {
                "text": text,
            },
        ],
        "properties": {
            "customized": False,
            "talkingAvatarCharacter": "lisa",
            "talkingAvatarStyle": "graceful-sitting",
            "videoFormat": "webm",
            "videoCodec": "vp9",
            "subtitleType": "soft_embedded",
            "backgroundColor": "transparent",
        }
    }

    response = requests.post(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        logger.info('Batch avatar synthesis job submitted successfully')
        logger.info(f'Job ID: {response.json()["id"]}')
        return response.json()["id"]
    else:
        logger.error(f'Failed to submit batch avatar synthesis job: {response.text}')
        st.error(f'Failed to submit batch avatar synthesis job: {response.text} Check SUBSCRIPTION_KEY or REGION')


def get_synthesis(job_id):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar/{job_id}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.debug('Get batch synthesis job successfully')
        logger.debug(response.json())
        if response.json()['status'] == 'Succeeded':
            logger.info(f'Batch synthesis job succeeded, download URL: {response.json()["outputs"]["result"]}')
            return response.json()["outputs"]["result"]
        return response.json()['status']
    else:
        logger.error(f'Failed to get batch synthesis job: {response.text}')
        st.error(f'Failed to get batch synthesis job: {response.text}')


def list_synthesis_jobs(skip: int = 0, top: int = 100):
    """List all batch synthesis jobs in the subscription"""
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar?skip={skip}&top={top}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.info(f'List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
        logger.info(response.json())
        return response.json()['values']
    else:
        logger.error(f'Failed to list batch synthesis jobs: {response.text}')
        st.error(f'No Avtar Video Jobs Exist')
        return []


def main():
    st.title("Text to Avatar Video Synthesis")

    text = st.text_area("Enter the text to be synthesized into avatar video:", "Hi, I'm a virtual assistant created by Microsoft.")

    if st.button("Submit"):
        job_id = submit_synthesis(text)
        if job_id:
            st.success(f"Job submitted successfully. Job ID: {job_id}")
            st.info("Waiting for job completion...")
            status = None
            while status not in ['Succeeded', 'Failed']:
                status = get_synthesis(job_id)
                if status == 'Succeeded':
                    download_url = get_synthesis(job_id)
                    st.success(f"Job succeeded! Download your video [here]({download_url})")
                    break
                elif status == 'Failed':
                    st.error("Job failed.")
                    break
                else:
                    st.info(f"Job status: {status}. Checking again in 5 seconds...")
                    time.sleep(5)

    st.header("List Batch Synthesis Jobs")
    jobs = list_synthesis_jobs()
    if jobs:
        st.write(f"Total jobs: {len(jobs)}")
        st.write("Job details:")
        for job in jobs:
            st.write(job)


if __name__ == '__main__':
    main()
