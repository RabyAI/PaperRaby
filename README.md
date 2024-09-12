# PaperRaby

## Overview
This open-source project aims to leverage artificial intelligence to enhance the efficiency of human research. By automating certain aspects of the research and writing process, we hope to empower researchers to focus more on innovative thinking and critical analysis.

## Getting Started
### Prerequisites
- Python 3.8+
- Dependencies listed in `requirements.txt`

### Installation
1. Clone the repository
2. Navigate to the project directory
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Add OpenAI (or ANTHROPIC) API key to the environment
   ```
   export OPENAI_API_KEY="YOUR KEY HERE"
   ```

   ```
   export ANTHROPIC_API_KEY="YOUR KEY HERE"
   ```

### Create Project
Create folder in templates and create below 3 files to begin with:
1. prompt.json
2. seed_ideas.json
3. data.csv (will be used as context for idea generation and data analysis)

## Features

### Automated research idea brainstorm

```
python launch_raby.py --project YOURPROJECT --model "claude-3-5-sonnet-20240620" --num-ideas 2 --idea-generation
```

### Research idea novelty check

Select one of the ideas-xxx.json and change filename to ideas.json
```
python launch_raby.py --project YOURPROJECT --model "claude-3-5-sonnet-20240620" --num-ideas 2 --check-novelty
```

### Data Collection

Enter the webpage URLs in data-from-web.txt, and execute the following command to analyze and collect data from the web. The results will be saved in different data-from-web-[].csv files.

```
python launch_raby.py --project YOURPROJECT --model "claude-3-5-sonnet-20240620" --collect-web-data
```

Name the PDF from which you want to extract data as data-from-pdf.pdf and place it in the project folder, then execute the following command to analyze and collect data from the PDF. The results will be saved in data-from-pdf.csv files.

```
python launch_raby.py --project YOURPROJECT --model "claude-3-5-sonnet-20240620" --collect-pdf-data
```

### Analysis data and create plots

Consolidate your target idea in templates/YOURPROJECT/ideas.json
Consolidate your data into data.csv file in templates/YOURPROJECT/data.csv
This feature will help to analysis data and create plots into results/YOURPROJECT/datetime_ideaname

```
python launch_raby.py --project YOURPROJECT --model "claude-3-5-sonnet-20240620" --experiment
```

### In the queue

- Automated literature review
- Citation management and formatting
- Outline generation for research papers
- Draft writing assistance

## License
This project is licensed under the Apache 2.0 License.

## Acknowledgments
- [AI-Scientist](https://github.com/SakanaAI/AI-Scientist)

## Disclaimer
This tool is designed to assist in the research process, not to replace human judgment or creativity. Users should always review and verify AI-generated content for accuracy and appropriateness.

## Contact
[Eric Yu] - [ericfish@gmail.com]