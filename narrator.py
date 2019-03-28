import time
import re

from section import Section
from eventSystem import EventHandler, EventConfig

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
    # Load Config
        self.loadConfig(config)
    # Event System
        self.eventHandler = EventHandler()
        self.eventHandler.subscribe("gameLoaded", self.fastForward)

        self.eventHandler.configureEvent("inputRequest", EventConfig.INSTANT)
        self.eventHandler.configureEvent("gameLoaded", EventConfig.INSTANT | EventConfig.SINGLE)
        self.eventHandler.configureEvent("narratorReady", EventConfig.INSTANT)
        self.eventHandler.configureEvent("step", EventConfig.INSTANT)
        self.eventHandler.configureEvent("print", EventConfig.INSTANT)
    #
    #####

    def start(self):
        
    #####
    # Load narration and previous state
        self.loadNarration()
        self.loadPreviousState()
    #
    #####
        if self.sectionToBe == "" or not self.eventHandler.scheduleEvent("gameLoaded"):
            self.startNewNarrative()

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

        self.alive = True
        self.eventHandler.scheduleEvent("narratorReady")


    def startNewNarrative(self):
        self.decisions = ""
        self.delayData["delayed"] = "False"
        self.delayData["target"] = "None"
        self.sectionToBe = ""
        
        self.setSection("initialize")

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
        with open(self.config["savePath"], 'r+') as saveFile:

            for line in saveFile:
                pair = line.strip().split("=")
                
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
        self.eventHandler.scheduleEvent("inputRequest", {"options": optionData, "callback": onInput})

    def fastForward(self, data):
        pass #TODO fast forward to last position

    def okay(self):
        return True