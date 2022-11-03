import subprocess
from edit_code_utils import *
from bash import *
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from skills.send_email import get_emails, send_email
from skills.create_file import create_new_file
from classify_text import select_classification_label
from aws_polly import main as aws_polly_tts
from open_ai import open_ai
import requests
import io
import json
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import click
import VRC_OSCLib
import websocket

temp_dir = tempfile.mkdtemp()
save_path = os.path.join(temp_dir, "temp.wav")

# some regular mistakenly recognized words/sentences on mostly silence audio, which are ignored in processing
blacklist = [
    "",
    "Thanks for watching!",
    "Thank you for watching!",
    "Thanks for watching.",
    "Thank you for watching.",
    "you",
    "..........................",
    "...",
]
# make all list entries lowercase for later comparison
blacklist = list((map(lambda x: x.lower(), blacklist)))

@click.command()
@click.option('--devices', default='False', help='print all available devices id', type=str)
@click.option('--device_index', default=-1, help='the id of the device (-1 = default active Mic)', type=int)
@click.option('--sample_rate', default=44100, help='sample rate of recording', type=int)
@click.option("--task", default="transcribe", help="task for the model whether to only transcribe the audio or translate the audio to english", type=click.Choice(["transcribe", "translate"]))
@click.option("--model", default="small", help="Model to use", type=click.Choice(["tiny","base", "small","medium","large"]))
@click.option("--english", default=False, help="Whether to use English model",is_flag=True, type=bool)
@click.option("--condition_on_previous_text", default=False, help="Feed it the previous result to keep it consistent across recognition windows, but makes it more prone to getting stuck in a failure loop",is_flag=True, type=bool)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True,type=bool)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False,is_flag=True, help="Flag to enable dynamic engergy", type=bool)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--phrase_time_limit", default=None, help="phrase time limit before entry ends to break up long recognitions.", type=float)
@click.option("--osc_ip", default="0", help="IP to send OSC message to. Set to '0' to disable", type=str)
@click.option("--websocket_ip", default="0", help="IP where Websocket Server listens on. Set to '0' to disable", type=str)



def main(devices, device_index, sample_rate, task, model, english, condition_on_previous_text, verbose, energy, pause,dynamic_energy, phrase_time_limit, osc_ip, websocket_ip):

    def select_email_recipient(text, emails):
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
        model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
        from transformers import pipeline
        classifier = pipeline("zero-shot-classification",
                            model="facebook/bart-large-mnli")


        sequence_to_classify = text
        # for each email, make a candidate label
        candidate_labels = ["the email should be sent to" + str(email) for email in emails]
        results = classifier(sequence_to_classify, candidate_labels)
        confidence = results['scores'][0]
        best_label = results['labels'][0]
        print(best_label, confidence)
        # it returns the email should be sent to{'name': 'Canyon Smith', 'email': ' canyonfsmith@gmail.com'} 0.8189042210578918
        # get the email from the best label
        email = best_label.split("to")[1]
        # convert to json
        print(email)
        # remove the spaces
        email = email.replace(" ", "")
        # try converting to json if it fails, try converting to dict
        try:
            # convert to json
            email = json.loads(email)
        except:
            # convert to dict
            email = eval(email)
        print("a",email)
        
        
        

        
        # email = json.loads(email)
        # now get the email address
        email = email['email']
        print(email)
        recipient = email
        
        return recipient

    def get_past_text():
        with open('open_ai_responses.txt', 'r') as f:
            lines = f.readlines()
            lines = lines[-10:]
            past_text = "".join(lines)
            return past_text

    if str2bool(devices) == True:
        index = 0
        for device in sr.Microphone.list_microphone_names():
            print(device, end = ' [' + str(index) + '] ' + "\n")
            index = index + 1
        return

    if websocket_ip != "0":
        websocket.StartWebsocketServer(websocket_ip, 5000)

    #there are no english models for large
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)    
    
    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=sample_rate, device_index=(device_index if device_index > -1 else None)) as source:
        print("Say something!")
        
        while True:
            #get and save audio to wav file
            audio = r.listen(source, phrase_time_limit=phrase_time_limit)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format="wav")

            if english:
                result = audio_model.transcribe(save_path, task=task, language='english', condition_on_previous_text=condition_on_previous_text)
            else:
                result = audio_model.transcribe(save_path, task=task, condition_on_previous_text=condition_on_previous_text)

            predicted_text = result.get('text').strip()
            print(predicted_text)   
            if predicted_text.lower() not in blacklist and predicted_text != "" and predicted_text != " " and "..." not in predicted_text and "jarvis" in predicted_text.lower():
                command, confidence  = select_classification_label(predicted_text)
                if command == "Do nothing":
                    pass

                    
                elif command == "Execute send text" and confidence > 0.9:
                    
                    print("sending text")
                    send = requests.post('https://hooks.zapier.com/hooks/catch/12053983/b0z2nmo/', json={"text": predicted_text})
                elif command == "Execute write python code":
                    print("writing python code")

                elif command == "Send email" and confidence > 0.9:
                    # execute send email from skills folder
                    print("sending email")
                    print(get_emails())
                    emails = get_emails()
                    past_text = get_past_text()
                    recipient = select_email_recipient(past_text, emails)
                    text_response = open_ai(past_text)
                    send_email(recipient, text_response)
                elif command == "Edit code":
                    predicted_text = predicted_text.replace("jarvis", "")
                    predicted_text = predicted_text.replace("edit", "")
                    predicted_text = predicted_text.replace("code", "")
                    print(predicted_text)
                    command = "code " + predicted_text
                    directory_contents, best_label, confidence = get_directory_contents(command)
                    file_name, function_name = select_function(best_label, command)
                    replace_function(function_name, file_name, edit_code(get_function_code(function_name, file_name),command))
                elif command == "Execute command":
                    
                    # execute subprocess command to run hello_world() from stake.py
                    print("executing command")
                    subprocess.call(['python3', 'stake.py','goodbye_world'])
                elif command == "Do me a favor":
                    command = predicted_text.replace("jarvis", "")
                    command = command.replace("do me a favor", "")
                    directory_contents, best_label, confidence = get_directory_contents(command)
                    file_name, function_name = select_function(best_label, command)
                    subprocess.call(['python3', file_name, function_name])
                    

                    
                    

                    
                    
                
            with open('open_ai_responses.txt', 'a') as f:
                f.write("Canyon: " + predicted_text + "\n")

            past_text = get_past_text()


            if not predicted_text.lower() in blacklist: 
                if not verbose and predicted_text != "":                    
                    print(("(Canyon))" if osc_ip != "0" else "") + ": " + predicted_text)
                    
                    text_response = open_ai(past_text)
                    print("OpenAI: " + text_response)
                    aws_polly_tts(text_response)

                else:
                    pass
                # if websocket_ip != "0":
                #     websocket.BroadcastMessage(json.dumps(result))

def str2bool(string):
    str2val = {"true": True, "false": False}
    if string.lower() in str2val:
        return str2val[string.lower()]
    else:
        raise ValueError(f"Expected one of {set(str2val.keys())}, got {string}")

main()


def get_past_text():
    with open('open_ai_responses.txt', 'r') as f:
        lines = f.readlines()
        lines = lines[-10:]
        past_text = "".join(lines)
        return past_text