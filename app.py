from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import requests, os, uuid, json
from flask import Flask, redirect, url_for, request, render_template, session

load_dotenv()
key = os.getenv("LANGUAGE_KEY")
endpoint = os.getenv("LANGUAGE_ENDPOINT")

#  Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
# Example method for summarizing text
def index_post():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        ExtractSummaryAction
    ) 
    original_text = request.form['text']
    document = [original_text]

    
    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count=4)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        summary = ([sentence.text for sentence in extract_summary_result.sentences])

    return render_template(
        'results.html', 
        document = document,
        summary = summary
        )
