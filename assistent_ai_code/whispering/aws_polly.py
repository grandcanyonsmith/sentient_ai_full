import os
from boto3 import client
import random
def aws_polly_tts(input_msg, name_id):
    polly = client('polly', region_name='us-west-2')

    response = polly.synthesize_speech(
            Text=input_msg,
            OutputFormat='mp3',
            VoiceId=name_id)

    stream = response.get('AudioStream')

    with open('output_aws_polly.mp3', 'wb') as f:
        data = stream.read()
        f.write(data)

def main(text_to_speech):
    
    input_msg = text_to_speech
    
    
    name_id_list = ['Joanna', 'Matthew', 'Brian', 'Amy', 'Emma', 'Raveena', 'Ivy', 'Joey', 'Justin', 'Kendra', 'Kimberly', 'Salli', 'Geraint', 'Mads', 'Naja', 'Hans', 'Marlene', 'Nicole', 'Russell', 'Conchita', 'Enrique', 'Miguel', 'Penelope', 'Chantal', 'Celine', 'Mathieu', 'Dora', 'Karl', 'Carla', 'Giorgio', 'Mizuki', 'Liv', 'Lotte', 'Ruben', 'Ewa', 'Jacek', 'Jan', 'Maja', 'Ricardo', 'Vitoria', 'Cristiano', 'Ines', 'Carmen', 'Maxim', 'Tatyana', 'Astrid', 'Filiz']
    # name the british voice
    
    name_id = 'Russell'

    aws_polly_tts(input_msg, name_id)

    # now play the audio file
    os.system("mpg321 output_aws_polly.mp3")


