import openai

def edit_code_temp(code, command, temp):
    """
    This function takes in a code and a command and returns the edited code.
    """
    openai.api_key = "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"
    response = openai.Edit.create(
    model="code-davinci-edit-001",
    input=code,
    instruction=command,
    temperature=temp,
    top_p=.9
    )
    new_code = response.choices[0].text
    return new_code


