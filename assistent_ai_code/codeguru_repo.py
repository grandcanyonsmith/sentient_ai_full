from pandas import DataFrame as df
# this file lists all the recommendations for the last pr that was made with aws codeguru-reviewer
import json
import boto3
import openai
from openai.embeddings_utils import cosine_similarity
import os
import csv
import time
from edit_code_utils import replace_function, get_function_code
import time
import os
import logging

from code_search_two import (
    create_data_frame,
    get_functions,
    get_line,
    search_functions,
)


codeguru = boto3.client('codeguru-reviewer')

def get_codeguru_recommendations(code_review_arn):
    """
    This function takes in a code review arn and returns the recommendations.
    """
    response = codeguru.list_recommendations(CodeReviewArn=code_review_arn)
    return response['RecommendationSummaries']


def edit_code(code, command):
    """
    This function takes in a code and a command and returns the edited code.
    """
    openai.api_key = "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"
    response = openai.Edit.create(
    model="code-davinci-edit-001",
    input=code,
    instruction=command,
    temperature=.8,
    top_p=1,
    )
    return response.choices[0].text


logger = logging.getLogger(__name__)


def write_to_file(recommendation, code, new_code):
        with open('changes.txt', 'a') as f:
            f.write(f"Changes\n{recommendation}\n\nOld Code:\n{code}\n\nNew Code:\n{new_code}\n\n\n")
            logger.info(f"Recommendation: {recommendation} | "
                        f"Old code: {code} | "
                        f"New code: {new_code} | "
                        f"\n")


def process_recommendation(recommendation_summaries):
    for summary in recommendation_summaries:

        recommendation_id = summary['RecommendationId']
        category = summary['RecommendationCategory']
        start_line = summary['StartLine']
        end_line = summary['EndLine']
        recommendation = summary['Description']
        file_path = summary['FilePath']
        severity = summary['Severity']

        logger.info(f"Recommendation ID: {recommendation_id} | "
                    f"Category: {category} | "
                    f"Recommendation: {recommendation} | "
                    f"Start line: {start_line} | "
                    f"End line: {end_line} | "
                    f"File path: {file_path} | "
                    f"Severity: {severity}\n")
        current_path = os.getcwd()
        file_path = os.path.join(current_path, file_path)
        line = get_line(file_path, start_line)
        funcs = list(get_functions(file_path))
        df = create_data_frame(funcs)
        functions, code = search_functions(
            df, line, n=1, pprint=True, n_lines=100)
        new_code = edit_code(code, 'Refactor this code to be pythonic.')

        new_code = edit_code(functions, 'Clean up this function to be pythonic. Follow PEP8 guidelines.')
        logger.info(f"Recommendation: {recommendation} | "
                    f"Old code: {code} | "
                    f"New code: {new_code} | "
                    f"\n")

        new_code = "\n\n" + new_code
        replace_function(functions, file_path, new_code)
        write_to_file('Refactor this code to be pythonic', code, new_code)



if __name__ == "__main__":
    code_review_arn = 'arn:aws:codeguru-reviewer:us-west-2:817842560692:association:2d4f68a7-02d7-476f-b24e-9a8bbef6e7c4:code-review:PullRequest-GITHUB-sentient_ai_full-1-e71a19d49d6c4864bcd8bbc63c0f0fbc818c8aba'
    recommendation_summaries = get_codeguru_recommendations(code_review_arn)
    process_recommendation(recommendation_summaries)