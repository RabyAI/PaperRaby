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
3. data.csv

## Features

### Automated research idea brainstorm

```
python launch_raby.py --project RabyAI --model "claude-3-5-sonnet-20240620" --num-ideas 2 --idea-generation
```

### Research idea novelty check

```
python launch_raby.py --project RabyAI --model "claude-3-5-sonnet-20240620" --num-ideas 2 --check-novelty
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