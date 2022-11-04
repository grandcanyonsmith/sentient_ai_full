import os
import openai

past_text = ""

def open_ai(past_text):
    openai.api_key = "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"
    prompt = past_text + "\nAI: "
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=.2,
    max_tokens=150,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0.4,
    )

    response = response.choices[0].text
    response = response[2:] # eliminate the \n\n at the beginning of the response

    with open('open_ai_responses.txt', 'a') as f:
        f.write(f"AI: {response}" + "\n")

    return response


