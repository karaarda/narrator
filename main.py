import time

class Narrator:
    def __init__(self):
        self.narrationLines = []
        self.cursorPos = 0
        self.ENDpos = 0
        self.narrationValues = {}
        self.nestingDegree = 0

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
            
            self.nestingDegree = 0

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
            return 0

        elif currentLine.startswith("OPTION"):
            options = []
            
            i = self.cursorPos

            while self.narrationLines[i].strip().startswith("OPTION"):                
                i += 1
                
                spacePos = currentLine.find(" ")
                separatorPos = currentLine.find("::")

                option = {}
                option["name"] = currentLine[separatorPos+2:spacePos]
                option["message"] = currentLine[spacePos+1:]

                options.append(option)

                self.cursorPos += 1
                currentLine = self.narrationLines[self.cursorPos]
                currentLine = currentLine.strip()

            for i in range(len(options)):
                print( i+1 , ". " , options[i]["message"] , sep='')

            userInput = int(input())

            userInput -= 1

            print("<" + options[userInput]["name"].strip() + ">")

            self.cursorPos = 0

            for line in self.narrationLines:
                if line.strip().startswith("<" + options[userInput]["name"].strip() + ">"):
                    break
                else:
                    self.cursorPos += 1

            return 0

        elif currentLine.startswith("IF"):
            currentLine = currentLine[2:]
            currentLine = currentLine.strip()

            isPos = currentLine.find("IS")

            leftValue = currentLine[0:isPos].strip()
            rightValue = currentLine[isPos + 2:].strip()

            print("right value: " + rightValue)
            print("left value: " + self.narrationValues[leftValue])

            if leftValue in self.narrationValues and self.narrationValues[leftValue] == rightValue:
                self.nestingDegree += 1
            else:
                dummy_nd = 0

                for i in range(self.cursorPos+1, len(self.narrationLines)):
                    if self.narrationLines[i].strip().startswith("END"):
                        if dummy_nd == 0:
                            self.cursorPos = i
                            break
                        else:
                            dummy_nd = dummy_nd - 1

                    elif self.narrationLines[i].strip().startswith("ELSE"):
                        if dummy_nd == 0:
                            self.cursorPos = i
                            break

                    elif self.narrationLines[i].strip().startswith("IF"):
                        dummy_nd = dummy_nd + 1
                # ???
                # try to find ELSE or END
                # if ELSE found, increase nesting degree
                # else do nothing.

            return self.narrate()
        elif currentLine.startswith("ELSE"):

            dummy_nd = 0

            for i in range(self.cursorPos+1, len(self.narrationLines)):
                if self.narrationLines[i].strip().startswith("END"):
                    if dummy_nd == 0:
                        self.cursorPos = i
                        break
                    else:
                        dummy_nd = dummy_nd - 1
                if self.narrationLines[i].strip().startswith("IF"):
                    dummy_nd = dummy_nd + 1

            #Find corresponding END
            #To do so skip over all lines
            #Find as many ENDs as the number of IF commands found
            return 0
        elif currentLine.startswith("END"):
            self.nestingDegree -= 1
            #decrease nesting degree
            pass

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