import os

# write a function that does the following:
# 1. asks for the user to input the variables found in the snippets below:
'''import os
import openai

past_text = ""

def open_ai(past_text):
    openai.api_key = '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'
    prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n" + past_text + "\nAI: "
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0,
    max_tokens=150,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0.2,
    )

    response = response.choices[0].text
    response = response[2:] # eliminate the \n\n at the beginning of the response
    
    with open('open_ai_responses.txt', 'a') as f:
        f.write("AI: " + response + "\n")
    
    return response'''
# 2. re writes the open_ai.py file with the new variables
# 3. executes the the bash command: python3 open_ai.py & echo $! > open_ai.pid


# Path: open_ai.py
# Compare this snippet from open_ai.py:
# import os
# import openai

past_text = ""

# variables to be replaced
prompt = input("prompt: ")
temperature = input("temperture: ")
max_tokens = input("Enter the max_tokens: ")
top_p = input("Enter the top_p: ")
frequency_penalty = input("Enter the frequency_penalty: ")
presence_penalty = input("Enter the presence_penalty: ")

saved_variables = [{"prompt": prompt}, {"temperature": temperature}, {"max_tokens": max_tokens}, {"top_p": top_p}, {"frequency_penalty": frequency_penalty}, {"presence_penalty": presence_penalty}]
# write the variables to a file to be read by the bash script
with open('open_ai_variables.csv', 'w') as f:
    for variable in saved_variables:
        # map the key and value to a string separated by a comma
        # with header variable, value
        f.write("variable, value\n")
        for key, value in variable.items():
            f.write(f"{key}, {value}" + "\n")



# def open_ai(past_text):
#     openai.api_key = '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'
#     prompt = prompt + '\n' + past_text + "\nAI: "
#     response = openai.Completion.create(
#     model="text-davinci-002",
#     prompt=prompt,
#     temperature=temperature,
#     max_tokens=max_tokens,
#     top_p=top_p,
#     frequency_penalty=frequency_penalty,
#     presence_penalty=presence_penalty,
#     )


new_code = '''
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
    openai.api_key = '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'
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
os.system('bash bash_script.sh & exit')'''

# with open('open_ai.py', 'w') as f:
# actually make a new file called open_ai_new.py
with open('open_ai_new.py', 'w') as f:
    f.write(new_code)



os.system("python3 open_ai_new.py & exit")
