import requests
from bs4 import BeautifulSoup
import csv
from raby.llm import get_response_from_llm

import os
import os.path as osp
import json

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


    # 获取网页内容
    for url in urls:
        response = requests.get(url)
        html_content = response.text

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取纯文本内容
        text_content = soup.get_text()

        # 向LLM发送请求
        msg = f"""You are a data analysis expert. Please parse the given web content related to data into structured tabular data. Convert the following web content into CSV format tabular data:
        {text_content}"""
    
        msg_history = []
        text, msg_history = get_response_from_llm(
            msg,
            client=client,
            model=model,
            system_message=idea_system_prompt,
            msg_history=msg_history,
        )
        # print(text)

        # 获取LLM的回复
        parsed_data = text

        # 将解析后的数据保存为CSV文件
        with open(osp.join(base_dir, f"data-from-web-{urls.index(url)}.csv"), 'w', newline='', encoding='utf-16') as csvfile:
            csvfile.write(parsed_data)

    print("Data has been successfully saved to the data-from-web file.")

