import re

class Section:
    
    def __init__(self, title):
        self.title = title
        self.lines = []
        self.cursorPos = 0
        self.nestingDegree = 0

    def restart(self):
        self.cursorPos = 0
        self.nestingDegree = 0

    def fastForward(self, narrator, input):
        pass

    def narrate(self, narrator):

        currentLine = self.lines[self.cursorPos]
        delay = 0

        if currentLine.startswith("PRINT"):
            self.command_print(narrator, currentLine[5:].strip())

        elif currentLine.startswith("GOTO"):
            self.command_goto(narrator, currentLine[4:].strip())

        elif currentLine.startswith("VAR"):
            self.command_var(narrator, currentLine[3:].strip())

        elif currentLine.startswith("OPTION"):
            self.command_option(narrator, currentLine)

        elif currentLine.startswith("DELAY"):
            delay = self.command_delay(narrator, currentLine[5:].strip())

            if narrator.config["fastForward"] == "True":
                delay = 0

        elif currentLine.startswith("IF"):
            self.command_if(narrator, currentLine[2:].strip())

        elif currentLine.startswith("ELSE"):
            self.command_else(narrator)

        elif currentLine.startswith("END"):
            self.command_end(narrator)

        if delay == 0:
            narrator.eventHandler.scheduleEvent("step")
        else:
            narrator.eventHandler.scheduleEvent("step", delay=delay)

    def get_action(self, command):
        pass

    def command_print(self, narrator, toPrint):
        narrator.eventHandler.scheduleEvent("print", {"message": toPrint})

        self.cursorPos += 1

    def command_goto(self, narrator, section):
        narrator.setSection(section)

    def command_var(self, narrator, dataString):
        data = dataString.split('=')
        narrator.narrationValues[data[0].strip()] = data[1].strip()

        self.cursorPos += 1

    def command_option(self, narrator, currentLine):
        options = []
        
        i = self.cursorPos

        while self.lines[i].startswith("OPTION"):                
            i += 1
            
            spacePos = currentLine.find(" ")
            separatorPos = currentLine.find("::")

            option = {}
            option["name"] = currentLine[separatorPos+2:spacePos]
            option["message"] = currentLine[spacePos+1:]

            options.append(option)

            self.cursorPos += 1

            if self.cursorPos < len(self.lines):
                currentLine = self.lines[self.cursorPos]
            else:
                break

        def onInput(userInput):
            narrator.setSection(options[userInput]["name"].strip())

            narrator.decisions += str(userInput)
            narrator.save()

            if narrator.config["debug"] == "True":
                print("<" + options[userInput]["name"].strip() + ">")

        narrator.requestInput( options, onInput)

    def command_delay(self, narrator, timeString): 
        hour = re.search("([1-9]{1}[0-9]{0,})h", timeString)
        minute = re.search("([1-9]{1}[0-9]{0,})m", timeString)
        second = re.search("([1-9]{1}[0-9]{0,})s", timeString)

        delay = 0

        if hour != None:
            delay += int(hour.group(1)) * 60 * 60
        if minute != None:
            delay += int(minute.group(1)) * 60
        if second != None:
            delay += int(second.group(1))

            self.cursorPos += 1

    def command_if(self, narrator, condition):
        conditionTokens = condition.split("IS")

        leftValue = conditionTokens[0]
        rightValue = conditionTokens[1]

        if narrator.config["debug"] == "True":
            print("right value: " + rightValue)
            print("left value: " + narrator.narrationValues[leftValue])

        if leftValue in narrator.narrationValues and narrator.narrationValues[leftValue] == rightValue:
            self.nestingDegree += 1
        else:
            dummy_nd = 0

            for i in range(self.cursorPos+1, len(self.lines)):
                if self.lines[i].startswith("END"):
                    if dummy_nd == 0:
                        self.cursorPos = i
                        break
                    else:
                        dummy_nd = dummy_nd - 1

                elif self.lines[i].startswith("ELSE"):
                    if dummy_nd == 0:
                        self.cursorPos = i
                        break

                elif self.lines[i].startswith("IF"):
                    dummy_nd = dummy_nd + 1
            # ???
            # try to find ELSE or END
            # if ELSE found, increase nesting degree
            # else do nothing.

        self.cursorPos += 1

        return self.narrate(narrator)

    def command_else(self, narrator):
        dummy_nd = 0

        for i in range(self.cursorPos+1, len(self.lines)):
            if self.lines[i].startswith("END"):
                if dummy_nd == 0:
                    self.cursorPos = i
                    break
                else:
                    dummy_nd = dummy_nd - 1
            if self.lines[i].startswith("IF"):
                dummy_nd = dummy_nd + 1

        #Find corresponding END
        #To do so skip over all lines
        #Find as many ENDs as the number of IF commands found

        self.cursorPos += 1

    def command_end(self, narrator):
        self.nestingDegree -= 1
        #decrease nesting degree

        self.cursorPos += 1