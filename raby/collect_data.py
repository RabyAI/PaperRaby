import requests
from bs4 import BeautifulSoup
import csv
from raby.llm import get_response_from_llm

import os
import os.path as osp
import json

from PyPDF2 import PdfReader
from datetime import datetime

web_data_prompt = """{task_description}
You are a data analysis expert. Please parse the given web content related to data into structured tabular data. Convert the following web content into CSV format tabular data:
{text_content}
"""

pdf_data_prompt = """{task_description}
You are a data analysis expert. Please parse the given PDF content related to data into structured tabular data. Convert the following PDF content into CSV format tabular data:
{text_content}
"""

def collect_data_from_web(
    base_dir,
    client,
    model
    ):

    with open(osp.join(base_dir, "prompt.json"), "r") as f:
        prompt = json.load(f)

    urls = []
    with open(osp.join(base_dir, "data-from-web.txt"), "r") as file:
        for line in file:
            urls.append(line.strip())

    idea_system_prompt = prompt["system"]


    # Get web content
    for url in urls:
        response = requests.get(url)
        html_content = response.text

        # Use BeautifulSoup to parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract plain text content
        text_content = soup.get_text()

        # Send request to LLM
        msg_history = []
        text, msg_history = get_response_from_llm(
            web_data_prompt.format(
                task_description=prompt["task_description"],
                text_content=text_content,
            ),
            client=client,
            model=model,
            system_message=idea_system_prompt,
            msg_history=msg_history,
        )

        # Get response from LLM
        parsed_data = text

        # Save parsed data as CSV file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(osp.join(base_dir, f"data-from-web-{timestamp}.csv"), 'w', newline='', encoding='utf-16') as csvfile:
            csvfile.write(parsed_data)

    print("Data has been successfully saved to the data-from-web file.")


def collect_data_from_pdf(base_dir, client, model):

    with open(osp.join(base_dir, "prompt.json"), "r") as f:
        prompt = json.load(f)

    idea_system_prompt = prompt["system"]

    # Read PDF file
    pdf_path = osp.join(base_dir, "data.pdf")
    pdf_reader = PdfReader(pdf_path)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += page.extract_text()

    # Send request to LLM
    msg_history = []
    text, msg_history = get_response_from_llm(
        pdf_data_prompt.format(
            task_description=prompt["task_description"],
            text_content=text_content,
        ),
        client=client,
        model=model,
        system_message=idea_system_prompt,
        msg_history=msg_history,
    )

    # Get response from LLM
    parsed_data = text

    # Save parsed data as CSV file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"data-from-pdf-{timestamp}.csv"
    with open(osp.join(base_dir, filename), 'w', newline='', encoding='utf-16') as csvfile:
        csvfile.write(parsed_data)

    print("Data has been successfully saved to the data-from-pdf file.")
