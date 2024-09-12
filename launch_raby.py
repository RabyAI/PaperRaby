import openai
import os.path as osp
import shutil
import json
import argparse
import multiprocessing
import torch
import os
import time
import sys
import csv
from datetime import datetime
from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput

from raby.generate_ideas import generate_ideas, check_idea_novelty
from raby.collect_data import collect_data_from_web, collect_data_from_pdf
from raby.perform_experiments import perform_experiments

NUM_REFLECTIONS = 3

def print_time():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Raby projects")
    # add type of project (nanoGPT, Boston, etc.)
    parser.add_argument(
        "--project",
        type=str,
        default="RabyAI",
        help="Research Project to run",
    )
    parser.add_argument(
        "--num-ideas",
        type=int,
        default=0,
        help="Number of ideas to generate",
    )
    parser.add_argument(
        "--idea-generation",
        default=False,
        action="store_true",
        help="Idea generation and load existing ideas",
    )
    parser.add_argument(
        "--check-novelty",
        default=False,
        action="store_true",
        help="Novelty check and use existing ideas",
    )
    parser.add_argument(
        "--collect-web-data",
        action="store_true",
        help="Read URLs from file and collect data from web",
    )
    parser.add_argument(
        "--collect-pdf-data",
        action="store_true",
        help="Read PDF from file and collect data from pdf",
    )
    parser.add_argument(
        "--experiment",
        default=False,
        action="store_true",
        help="Experiment to run.",
    )
    parser.add_argument(
        "--writeup",
        default=False,
        action="store_true",
        help="Write the paper.",
    )
    parser.add_argument(
        "--improvement",
        default=False,
        action="store_true",
        help="Improve the paper.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-5-sonnet-20240620",
        choices=[
            "claude-3-5-sonnet-20240620",
            "gpt-4o-2024-05-13",
            "deepseek-coder-v2-0724",
            "llama3.1-405b",
            # Anthropic Claude models via Amazon Bedrock
            "bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
            "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            "bedrock/anthropic.claude-3-haiku-20240307-v1:0",
            "bedrock/anthropic.claude-3-opus-20240229-v1:0"
            # Anthropic Claude models Vertex AI
            "vertex_ai/claude-3-opus@20240229",
            "vertex_ai/claude-3-5-sonnet@20240620",
            "vertex_ai/claude-3-sonnet@20240229",
            "vertex_ai/claude-3-haiku@20240307",
        ],
        help="Model to use for AI Scientist.",
    )
    return parser.parse_args()


def do_experiment(
    base_dir,
    results_dir,
    idea,
    model,
    client,
    client_model,
    writeup,
    improvement,
    log_file=False,
):
    ## CREATE PROJECT FOLDER
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    idea_name = f"{timestamp}_{idea['Name']}"
    folder_name = osp.join(results_dir, idea_name)
    assert not osp.exists(folder_name), f"Folder {folder_name} already exists."
    destination_dir = folder_name
    shutil.copytree(base_dir, destination_dir, dirs_exist_ok=True)

    with open(osp.join(base_dir, "data.csv"), "r") as f:
        baseline_results = f.read()
    # with open(osp.join(base_dir, "data.csv"), "r") as f:
    #     reader = csv.DictReader(f)
    #     baseline_results = json.dumps([row for _, row in zip(range(200), reader)])

    vis_file = osp.join(folder_name, "plot.py")
    notes = osp.join(folder_name, "notes.txt")
    with open(notes, "w") as f:
        f.write(f"# Title: {idea['Title']}\n")
        f.write(f"# Experiment description: {idea['Experiment']}\n")
        f.write(f"## Run 0: Baseline\n")
        f.write(f"Results: {baseline_results}\n")
        f.write(f"Description: Baseline results.\n")
    if log_file:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        log_path = osp.join(folder_name, "log.txt")
        log = open(log_path, "a")
        sys.stdout = log
        sys.stderr = log
    try:
        print_time()
        print(f"*Starting idea: {idea_name}*")

        fnames = [vis_file, notes]
        
        io = InputOutput(
            yes=True, chat_history_file=f"{folder_name}/{idea_name}_aider.txt"
        )
        if model == "deepseek-coder-v2-0724":
            main_model = Model("deepseek/deepseek-coder")
        elif model == "llama3.1-405b":
            main_model = Model("openrouter/meta-llama/llama-3.1-405b-instruct")
        else:
            main_model = Model(model)
        coder = Coder.create(
            main_model=main_model,
            fnames=fnames,
            io=io,
            stream=False,
            use_git=False,
            edit_format="diff",
        )

        print_time()
        print(f"*Starting Experiments*")
        try:
            success = perform_experiments(idea, folder_name, coder, baseline_results)
        except Exception as e:
            print(f"Error during experiments: {e}")
            print(f"Experiments failed for idea {idea_name}")
            return False

        if not success:
            print(f"Experiments failed for idea {idea_name}")
            return False

        # print_time()
        # print(f"*Starting Writeup*")
        # ## PERFORM WRITEUP
        # if writeup == "latex":
        #     writeup_file = osp.join(folder_name, "latex", "template.tex")

        #     if model == "deepseek-coder-v2-0724":
        #         main_model = Model("deepseek/deepseek-coder")
        #     elif model == "llama3.1-405b":
        #         main_model = Model("openrouter/meta-llama/llama-3.1-405b-instruct")
        #     else:
        #         main_model = Model(model)
        #     coder = Coder.create(
        #         main_model=main_model,
        #         fnames=fnames,
        #         io=io,
        #         stream=False,
        #         use_git=False,
        #         edit_format="diff",
        #     )
        #     try:
        #         perform_writeup(idea, folder_name, coder, client, client_model)
        #     except Exception as e:
        #         print(f"Failed to perform writeup: {e}")
        #         return False
        #     print("Done writeup")
        # else:
        #     raise ValueError(f"Writeup format {writeup} not supported.")

        # print_time()
        # print(f"*Starting Review*")
        # ## REVIEW PAPER
        # if writeup == "latex":
        #     try:
        #         paper_text = load_paper(f"{folder_name}/{idea['Name']}.pdf")
        #         review = perform_review(
        #             paper_text,
        #             model="gpt-4o-2024-05-13",
        #             client=openai.OpenAI(),
        #             num_reflections=5,
        #             num_fs_examples=1,
        #             num_reviews_ensemble=5,
        #             temperature=0.1,
        #         )
        #         # Store the review in separate review.txt file
        #         with open(osp.join(folder_name, "review.txt"), "w") as f:
        #             f.write(json.dumps(review, indent=4))
        #     except Exception as e:
        #         print(f"Failed to perform review: {e}")
        #         return False

        # ## IMPROVE WRITEUP
        # if writeup == "latex" and improvement:
        #     print_time()
        #     print(f"*Starting Improvement*")
        #     try:
        #         perform_improvement(review, coder)
        #         generate_latex(
        #             coder, folder_name, f"{folder_name}/{idea['Name']}_improved.pdf"
        #         )
        #         paper_text = load_paper(f"{folder_name}/{idea['Name']}_improved.pdf")
        #         review = perform_review(
        #             paper_text,
        #             model="gpt-4o-2024-05-13",
        #             client=openai.OpenAI(),
        #             num_reflections=5,
        #             num_fs_examples=1,
        #             num_reviews_ensemble=5,
        #             temperature=0.1,
        #         )
        #         # Store the review in separate review.txt file
        #         with open(osp.join(folder_name, "review_improved.txt"), "w") as f:
        #             f.write(json.dumps(review))
        #     except Exception as e:
        #         print(f"Failed to perform improvement: {e}")
        #         return False
        # return True
    except Exception as e:
        print(f"Failed to evaluate idea {idea_name}: {str(e)}")
        return False
    finally:
        print("FINISHED IDEA")
        if log_file:
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            log.close()

if __name__ == "__main__":
    args = parse_arguments()

    # Create client
    if args.model == "claude-3-5-sonnet-20240620":
        import anthropic

        print(f"Using Anthropic API with model {args.model}.")
        client_model = "claude-3-5-sonnet-20240620"
        client = anthropic.Anthropic()
    elif args.model.startswith("bedrock") and "claude" in args.model:
        import anthropic

        # Expects: bedrock/<MODEL_ID>
        client_model = args.model.split("/")[-1]

        print(f"Using Amazon Bedrock with model {client_model}.")
        client = anthropic.AnthropicBedrock(
            aws_access_key=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_region=os.getenv("AWS_REGION_NAME"),
        )
    elif args.model.startswith("vertex_ai") and "claude" in args.model:
        import anthropic

        # Expects: vertex_ai/<MODEL_ID>
        client_model = args.model.split("/")[-1]

        print(f"Using Vertex AI with model {client_model}.")
        client = anthropic.AnthropicVertex()
    elif args.model == "gpt-4o-2024-05-13":
        import openai

        print(f"Using OpenAI API with model {args.model}.")
        client_model = "gpt-4o-2024-05-13"
        client = openai.OpenAI()
    elif args.model == "deepseek-coder-v2-0724":
        import openai

        print(f"Using OpenAI API with {args.model}.")
        client_model = "deepseek-coder-v2-0724"
        client = openai.OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com"
        )
    elif args.model == "llama3.1-405b":
        import openai

        print(f"Using OpenAI API with {args.model}.")
        client_model = "meta-llama/llama-3.1-405b-instruct"
        client = openai.OpenAI(
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1",
        )
    else:
        raise ValueError(f"Model {args.model} not supported.")

    base_dir = osp.join("templates", args.project)
    results_dir = osp.join("results", args.project)

    if args.num_ideas > 0:
        ideas = generate_ideas(
            base_dir,
            client=client,
            model=client_model,
            generation=args.idea_generation,
            max_num_generations=args.num_ideas,
            num_reflections=NUM_REFLECTIONS,
        )

        ideas = check_idea_novelty(
            ideas,
            base_dir=base_dir,
            client=client,
            model=client_model,
            novelty_check=args.check_novelty,
        )

    if args.collect_web_data:
        collect_data_from_web(
            base_dir=base_dir,
            client=client,
            model=client_model,
        )
        
    if args.collect_pdf_data:
        collect_data_from_pdf(
            base_dir=base_dir,
            client=client,
            model=client_model,
        )


    if args.experiment:
        
        # with open(osp.join(base_dir, "ideas.json"), "w") as f:
        #     json.dump(ideas, f, indent=4)
        # novel_ideas = [idea for idea in ideas if idea["novel"]]

        with open(osp.join(base_dir, "ideas.json"), "r") as f:
            ideas = json.load(f)
        novel_ideas = [idea for idea in ideas]

        for idea in novel_ideas:
            print(f"Processing idea: {idea['Name']}")
        try:
            success = do_experiment(
                base_dir,
                results_dir,
                idea,
                args.model,
                client,
                client_model,
                args.writeup,
                args.improvement,
                # True
            )
            print(f"Completed idea: {idea['Name']}, Success: {success}")
        except Exception as e:
            print(f"Failed to evaluate idea {idea['Name']}: {str(e)}")