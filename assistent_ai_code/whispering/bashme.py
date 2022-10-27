
# python3 audioWhisper.py & exit 0
# touch test.txt
# exit 0
# python3 audioWhisper.py & exit 0
import subprocess
import time
# path /Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/audioWhisper.py
def execute():
    # run audio whisper and  /Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/wait.py'])
    subprocess.call(['python3', '/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/audioWhisper.py'])
    #
    # exit the process
    exit(0)
    subprocess.call(['touch', '/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/test.txt'])
    # wait 5 seconds
    time.sleep(5)
    # run the python script again
    # exit the program
    subprocess.call(['exit', '0'])
    subprocess.call(['python3', '/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/audioWhisper.py'])
    

execute()