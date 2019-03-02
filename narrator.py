import time
import re

from section import Section

class Narrator:
    def __init__(self, config="default.conf"):
    #####
    # Member Variables
        self.config = {}
        self.sections = []
        self.currentSection = None
        self.sectionToBe = ""

        self.delayData = { "delayed": "False", "target": "None" }

        self.narrationValues = {}
        self.decisions = ""
    # Listeners
        self.onInputListener = None
    #
    #####

    #####
    # Load config and preivous state
        self.loadConfig(config)
        self.loadNarration()

        self.loadPreviousState()
    #
    #####

        self.setSection("initialize")

    #####
    # Fast-Forward to previous position
        # if self.decisions != "" or self.sectionToBe != "":
        #     i = 0

        #     while i < len(self.decisions) or self.currentSection.title != self.sectionToBe:
        #         decisionMade = self.currentSection.fastForward(self, self.decisions[i])

        #         if decisionMade:
        #             i += 1
    #
    #####

    def loadConfig(self, config):
        with open(config) as configFile:

            currentSetting = None

            for line in configFile:
                currentSetting = line.strip().split('=')
                self.config[currentSetting[0]] = currentSetting[1]

    def loadNarration(self):
        with open(self.config["narrationPath"]) as narrationFile:

            currentSection = None

            for line in narrationFile:
                sectionTitle = re.search("<(\w+)>", line)

                if sectionTitle != None:
                    currentSection = Section(sectionTitle.group(1))

                elif line.strip().startswith("</>"):
                    self.sections.append(currentSection)

                else:
                    currentSection.lines.append(line.strip())

    def setSection(self, sectionTitle):
        for section in self.sections:
            if section.title == sectionTitle:
                self.currentSection = section
                self.currentSection.restart()
                break

        self.save()

    def loadPreviousState(self):
        #reload previous state of the narrative
        with open(self.config["savePath"], 'a+') as saveFile:

            for line in saveFile:
                pair = line.split("=")
                
                if pair[0] == "decisions":
                    self.decisions = pair[1]
                elif pair[0] == "delayed":
                    self.delayData["delayed"] = pair[1]
                elif pair[0] == "target":
                    self.delayData["target"] = pair[1]
                elif pair[0] == "section":
                    self.sectionToBe = pair[1]

    def save(self, manuel = False):
        if manuel or self.config["autoSave"] == "True":
            with open(self.config["savePath"], 'w+') as saveFile:
                saveFile.write("decisions=" + self.decisions + "\n")
                saveFile.write("section=" + self.currentSection.title + "\n")
                saveFile.write("delayed=" + self.delayData["delayed"] + "\n")
                saveFile.write("target=" + self.delayData["target"])

    def narrate(self):
        return self.currentSection.narrate(self)

    def requestInput(self, optionData, onInput):
        if( self.onInputListener != None ):
            self.onInputListener(optionData, onInput)

    def okay(self):
        return True