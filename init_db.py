import json
import traceback

import libyuki

try:
    with open("guildsettings.json", "r", encoding="utf8") as f:
        guildsettings = json.load(f)
    with open("txtMsg.json", "r") as f:
        txtMsg = json.load(f)
    with open("vcTxt.json", "r") as f:
        vcTxt = json.load(f)
    with open("vcRole.json", "r") as f:
        vcRole = json.load(f)
except:
    traceback.print_exc()