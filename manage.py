import argparse


from faceapp.datagathering import register
from faceapp.Recognizer import recognize
from faceapp.speech import speak
from faceapp.doorlock import open_door
from faceapp.sms import send_sms


parser = argparse.ArgumentParser(description='Welcome to David Face recog', \
    exit_on_error=False)


parser.add_argument('-r', "--register", action="store_true", help='register a new face')
parser.add_argument('-d', "--detect", action="store_true", help='detect a face')
parser.add_argument('-g', "--gui", action="store_true", help='start gui')
parser.add_argument('-t', "--test_sms", action="store_true", help='test sms service')


args = parser.parse_args()


if args.test_sms:
    from settings import settings
    receivers = settings.PHONE_NUMBERS
    
    status = send_sms(to=receivers, msg='I am just testing this number. Dont freak out.')
    print(status)


if args.gui:
    from webapp import app
    if __name__ == "__main__":
        app.run()


if args.register:
    # registration logic
    print("Registration for a new face")
    speak("Registration for a new face")
    
    name = input("Enter a name: ")
    register(name)
    
    print("registration is done")
    speak("registration is done")

elif args.detect:
    # detection logic
    print("Starting face recognition")
    speak("Starting face recognition")
    
    name = recognize()
    
    if name == None:
        print(f"User unrecognized")
        speak(f"User unrecognized")
        
    else:
        open_door("1")
        print(f"Welcome in {name}")
        speak(f"Welcome in {name}")