# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# Based on anki code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Source in https://github.com/Arthur-Milchior/anki-json-new-line
# Addon number 11201952
from aqt.addons import AddonManager, ConfigEditor
import sys
import json

oldLoads=json.loads
def newLoads(t,*args,**kwargs):
    t=correctJson(t)
    return oldLoads(t,*args,**kwargs)

json.loads=newLoads

def debug(text):
    pass

def correctJson(text):
    l=[]
    numberOfSlashOdd=False
    numberOfQuoteOdd=False
    for char in text:
        if char == "\n" and numberOfQuoteOdd:
            l.append("\\n")
            debug("adding \\n")
        else:
            l.append(char)
            if char=="\n":
                char="newline"
            debug(f"adding {char}")
            
        if char == "\"":
            if not numberOfSlashOdd:
                numberOfQuoteOdd = not numberOfQuoteOdd
                debug(f"numberOfQuoteOdd is now {numberOfQuoteOdd}")
                
        if char == "\\":
            numberOfSlashOdd = not numberOfSlashOdd
        else:
            numberOfSlashOdd = False
        debug(f"numberOfSlashOdd is now {numberOfSlashOdd}")
    return "".join(l)

def readableJson(text):
    l=[]
    numberOfSlashOdd=False
    numberOfQuoteOdd=False
    for char in text:
        if char == "n" and numberOfQuoteOdd and numberOfSlashOdd:
            l[-1]="\n"
            debug("replacing last slash by newline")
        else:
            l.append(char)
            if char=="\n":
                char="newline"
            debug(f"adding {char}")
            
        if char == "\"":
            if not numberOfSlashOdd:
                numberOfQuoteOdd = not numberOfQuoteOdd
                debug(f"numberOfQuoteOdd is now {numberOfQuoteOdd}")
                
        if char == "\\":
            numberOfSlashOdd = not numberOfSlashOdd
        else:
            numberOfSlashOdd = False
        debug(f"numberOfSlashOdd is now {numberOfSlashOdd}")
    return "".join(l)



def updateText(self, conf):
    self.form.editor.setPlainText(
        readableJson(json.dumps(conf,sort_keys=True,indent=4, separators=(',', ': '))))
ConfigEditor.updateText=updateText
