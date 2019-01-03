import time

class Narrator:
    def __init__(self):
        self.narrationLines = []
        self.cursorPos = 0
        self.narrationValues = {}

        self.loadNarration()
        self.loadPreviousState()

    def loadNarration(self):
        with open("data/narration.txt", encoding='utf-16') as narrationFile:
            
            startFound = False

            for line in narrationFile:
                if not startFound and not line.strip().startswith("<start>"):
                    self.cursorPos += 1
                else:
                    startFound = True

                self.narrationLines.append(line) 

    def loadPreviousState(self):
        pass
        #reload previous state of the narrative

    def narrate(self):
        self.cursorPos += 1

        currentLine = self.narrationLines[self.cursorPos]

        currentLine = currentLine.strip()

        if currentLine.startswith("PRINT"):
            currentLine = currentLine[5:]
            currentLine = currentLine.strip()
            print(currentLine)

            return 2
        elif currentLine.startswith("GOTO"):
            currentLine = currentLine[4:]
            currentLine = currentLine.strip()

            self.cursorPos = 0
        
            for line in self.narrationLines:
                if line.strip().startswith("<" + currentLine + ">"):
                    break
                else:
                    self.cursorPos += 1

            return 0

        elif currentLine.startswith("VAR"):
            currentLine = currentLine[3:]
            currentLine = currentLine.strip()

            equalityPos = currentLine.find("=")

            name = currentLine[0:equalityPos].strip()
            value = currentLine[equalityPos+1:].strip()

            self.narrationValues[name] = value
            print(self.narrationValues)
            return 0

        return 0
        #move cursor to the next position and interpret
        #take necessary actions and save the game status

    def okay(self):
        if self.cursorPos >= len(self.narrationLines):
            return False
        
        return True

def main():
    global narrator

    if not narrator.okay():
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