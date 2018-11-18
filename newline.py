# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# Based on anki code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Source in https://github.com/Arthur-Milchior/anki-json-new-line
# Addon number ????????????
from aqt.addons import AddonManager, ConfigEditor
import sys
import json

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

def addonMeta(self, dir):
    print(f"calling addonMeta({dir})")
    path = self._addonMetaPath(dir)
    try:
        with open(path, encoding="utf8") as f:
            t=f.read()
            t=correctJson(t)
            j=json.loads(t)
            if not isinstance(j, dict):
                raise Exception(f"Invalid configuration {j} in {dir}.")
            return j
    except:
        return dict()
AddonManager.addonMeta=addonMeta

def writeAddonMeta(self, dir, meta):
    path = self._addonMetaPath(dir)
    meta=json.dumps(meta)
    meta=readableJson(meta)
    with open(path, "w", encoding="utf8") as f:
        f.write(meta)
#AddonManager.writeAddonMeta=writeAddonMeta

def updateText(self, conf):
    self.form.editor.setPlainText(
        readableJson(json.dumps(conf,sort_keys=True,indent=4, separators=(',', ': '))))
ConfigEditor.updateText=updateText
    
def accept(self):
    txt = self.form.editor.toPlainText()
    try:
        new_conf = json.loads(correctJson(txt))
        if not isinstance(new_conf, dict):
            showInfo(_("Invalid configuration: Configurations should be dictionnaries."))
            return
    except Exception as e:
        showInfo(_("Invalid configuration: ") + repr(e))
        return

    if new_conf != self.conf:
        self.mgr.writeConfig(self.addon, new_conf)
        # does the add-on define an action to be fired?
        act = self.mgr.configUpdatedAction(self.addon)
        if act:
            act(new_conf)
        
    super(ConfigEditor,self).accept()
ConfigEditor.accept=accept