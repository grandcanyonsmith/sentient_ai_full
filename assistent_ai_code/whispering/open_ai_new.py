
import os
import openai
import time

# get the variables from the file open_ai_variables.csv
with open('open_ai_variables.csv', 'r') as f:
# skip the first line
    next(f)
    for line in f:
        # split the line into a list
        line = line.split(', ')
        # assign the variable to the value
        if line[0] == 'prompt':
            prompt = line[1]
        elif line[0] == 'temperature':
            temperature = line[1]
        elif line[0] == 'max_tokens':
            max_tokens = line[1]
        elif line[0] == 'top_p':
            top_p = line[1]
        elif line[0] == 'frequency_penalty':
            frequency_penalty = line[1]
        elif line[0] == 'presence_penalty':
            presence_penalty = line[1]
# remove the newline character from the end of the string
prompt = prompt[:-1]
temperature = temperature[:-1]
max_tokens = max_tokens[:-1]
top_p = top_p[:-1]
frequency_penalty = frequency_penalty[:-1]
presence_penalty = presence_penalty[:-1]
# convert the strings to the correct data type
temperature = float(temperature)
max_tokens = int(max_tokens)
top_p = float(top_p)
frequency_penalty = float(frequency_penalty)
presence_penalty = float(presence_penalty)


past_text = ""
def open_ai(past_text, prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
    openai.api_key = "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"
    prompt = prompt + past_text + "AI: ",
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=temperature,
    max_tokens=max_tokens,
    top_p=top_p,
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty,
    )
    response = response.choices[0].text
    response = response[2:] # eliminate the
    
    with open('open_ai_responses_new_new.txt', 'a') as f:
        f.write("AI: " + response)
    
    return response

new_code = open_ai(past_text, prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty)

# write the new code to the file new_function.py
with open('new_function.py', 'w') as f:
    f.write(new_code)

time.sleep(5)

# execute the new code in the file bash_script.sh
os.system('bash bash_script.sh & exit')