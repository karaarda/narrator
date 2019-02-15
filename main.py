import time

from narrator import Narrator

def main():
    global narrator

    if not narrator.okay():
        #TODO show error message
        exit()

    while not end:
        delay = narrator.narrate()
        time.sleep(delay)

if __name__ == "__main__":
    global narrator 
    narrator = Narrator()

    global end
    end = False

    main()