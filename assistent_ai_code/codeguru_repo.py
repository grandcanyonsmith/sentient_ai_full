from pandas import DataFrame as df
# this file lists all the recommendations for the last pr that was made with aws codeguru-reviewer
import json
import boto3
import openai
from openai.embeddings_utils import cosine_similarity
import os
import csv
import time
# from edit_code_utils import replace_function, get_function_code
import time
import os
import logging
from datetime import datetime

from code_search_two import (
    create_data_frame,
    get_functions,
    get_line,
    search_functions,
)

openai.api_key = "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"
codeguru = boto3.client('codeguru-reviewer')

def get_codeguru_recommendations(code_review_arn):
    """
    This function takes in a code review arn and returns the recommendations.
    """
    response = codeguru.list_recommendations(CodeReviewArn=code_review_arn)
    return response['RecommendationSummaries']

def list_codeguru_reviews():
    """
    This function takes in a type and returns all the code reviews for that type.
    """
    '''        {
            "Name": "grandcanyonsmith_sentient_ai-main-cffeb254-40be-42c7-8db6-39ae44e0c39e",
            "CodeReviewArn": "arn:aws:codeguru-reviewer:us-west-2:817842560692:association:c08b7476-d89e-4b10-8dbc-8b7dd452e0f8:code-review:RepositoryAnalysis-grandcanyonsmith_sentient_ai-main-cffeb254-40be-42c7-8db6-39ae44e0c39e",
            "RepositoryName": "sentient_ai",
            "Owner": "grandcanyonsmith",
            "ProviderType": "GitHub",
            "State": "Completed",
            "CreatedTimeStamp": 1667502392.6,
            "LastUpdatedTimeStamp": 1667502693.645,
            "Type": "RepositoryAnalysis",
            "MetricsSummary": {
                "MeteredLinesOfCodeCount": 0,
                "SuppressedLinesOfCodeCount": 0,
                "FindingsCount": 0
            },
            "SourceCodeType": {
                "RepositoryHead": {
                    "BranchName": "main"
                },
                "RequestMetadata": {}
            }
        }
    ]
}'''
    response = codeguru.list_code_reviews(Type='RepositoryAnalysis')
    reviews = []
    for review in response['CodeReviewSummaries']:
        
        # print(review)
        repository_name = review['RepositoryName']
        state = review['State']
        last_updated = review['LastUpdatedTimeStamp']
        
        
        # 2022-11-04 09:55:05.117000-06:00 <class 'datetime.datetime'>
        # convert to epoch
        last_updated = last_updated.timestamp()
        

        now = time.time()
        last_updated = now - last_updated
        # convert to minutes
        last_updated = int(last_updated) / 60
        
        # round to 2 decimal places
        last_updated = round(last_updated, 1)
        # if hours, convert to hours
        if last_updated > 60:
            last_updated = last_updated / 60
            last_updated = round(last_updated, 1)
            last_updated_time = f"{last_updated} hours ago"
        elif last_updated > 1440:
            last_updated = last_updated / 1440
            last_updated = round(last_updated, 1)
            last_updated_time = f"{last_updated} days ago"
            
        else:

            # round to 0 decimal places
            last_updated = round(last_updated, 0)
            last_updated_time = f"{last_updated} minutes ago"


        code_review_arn = review['CodeReviewArn']
        metrics_summary = review['MetricsSummary']['FindingsCount'] if state == 'Completed' else 0
        
        
        reviews.append({"repository_name": repository_name, "state": state, "last_updated": last_updated_time, "code_review_arn": code_review_arn, "metrics_summary": metrics_summary, "reviews": {}})
        
    return reviews




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




def write_to_file(recommendation, code, new_code):
        with open('changes.txt', 'a') as f:
            f.write(f"Changes\n{recommendation}\n\nOld Code:\n{code}\n\nNew Code:\n{new_code}\n\n\n")
            (logging.getLogger(__name__)).info(f"Recommendation: {recommendation} | "
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

        (logging.getLogger(__name__)).info(f"Recommendation ID: {recommendation_id} | "
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

        new_code = edit_code(functions, recommendation)
        (logging.getLogger(__name__)).info(f"Recommendation: {recommendation} | "
                    f"Old code: {code} | "
                    f"New code: {new_code} | "
                    f"\n")

        new_code = "\n\n" + new_code
        replace_function(functions, file_path, new_code)
        write_to_file(recommendation, code, new_code)



if __name__ == "__main__":
    # code_review_arn = 'arn:aws:codeguru-reviewer:us-west-2:817842560692:association:2d4f68a7-02d7-476f-b24e-9a8bbef6e7c4:code-review:RepositoryAnalysis-grandcanyonsmith_sentient_ai_full-canyon-patch-1-d6c13675-7826-4f34-b125-12e80c21c905'
    # recommendation_summaries = get_codeguru_recommendations(code_review_arn)
    # process_recommendation(recommendation_summaries)
    print("Getting codeguru reviews")
    reviews = list_codeguru_reviews()
    # print(reviews)

    # {'Name': 'grandcanyonsmith_accounting_ynab-main-c83bafd1-728b-40ab-8e24-cf3ba7bb3beb', 'CodeReviewArn': 'arn:aws:codeguru-reviewer:us-west-2:817842560692:association:c309c8b4-b547-4dbc-93af-123d753e08b3:code-review:RepositoryAnalysis-grandcanyonsmith_accounting_ynab-main-c83bafd1-728b-40ab-8e24-cf3ba7bb3beb', 'RepositoryName': 'accounting_ynab', 'Owner': 'grandcanyonsmith', 'ProviderType': 'GitHub', 'State': 'Failed', 'CreatedTimeStamp': datetime.datetime(2022, 11, 4, 9, 54, 0, 241000, tzinfo=tzlocal()), 'LastUpdatedTimeStamp': datetime.datetime(2022, 11, 4, 9, 55, 5, 117000, tzinfo=tzlocal()), 'Type': 'RepositoryAnalysis', 'SourceCodeType': {'RepositoryHead': {'BranchName': 'main'}, 'RequestMetadata': {}}}
    # pretty_print(reviews)
    for review in reviews:
        all_recommendations = []
        try:
            recommendation_summaries = get_codeguru_recommendations(review['code_review_arn'])
            all_recommendations.append(recommendation_summaries)
            amount = len(recommendation_summaries)
            # append the recommendations to the review
            review['recommendations'] = recommendation_summaries if amount > 0 else None
            review['recommendations_amount'] = amount  
        except Exception as e:
            review['recommendations'] = 0
            review['recommendations_amount'] = 0
            continue
        # apend the list of recommendations to the review
        review['reviews'] = all_recommendations
        
    
        
    
    print("Getting recommendations")
    # print(reviews)
    # pretty print the reviews. For each print the key once and all the values
    for review in reviews:
        print(review['repository_name'] + " (" + str(review['last_updated']) + ")" + "\n- " + str(review['recommendations_amount']) + " recommendations")
        try:
            i = 0
            for recommendation in range(len(review['recommendations'])):
                print("  - " +  review['recommendations'][i]['RecommendationCategory']+"\n")
                i += 1
            print("\n")
        except:
            pass
    

    