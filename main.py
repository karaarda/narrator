import time

from narrator import Narrator

def main():
    global narrator

    if not narrator.okay():
        #TODO show error message
        exit()

    while not end:
        delay = narrator.narrate()()
        time.sleep(delay)

def onInputListener(options, onInput):

    for i in range(len(options)):
        print( i, ". " , options[i]["message"] , sep='')

    userInput = int(input())

    onInput(userInput)

if __name__ == "__main__":
    global narrator 
    narrator = Narrator()
    narrator.onInputListener = onInputListener

    global end
    end = False

    main()