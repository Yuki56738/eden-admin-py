import json
import traceback

import libyuki

try:
    with open("guildsettings.json", "r", encoding="utf8") as f:
        guildsettings = json.load(f)
        libyuki.push_guilddb(id="guildsettings", payload=guildsettings)
    with open("txtMsg.json", "r") as f:
        txtMsg = json.load(f)
        libyuki.push_guilddb(id="txtMsg", payload=txtMsg)
        # libyuki.push_guilddb()
    with open("vcTxt.json", "r") as f:
        vcTxt = json.load(f)
        libyuki.push_guilddb(id="vcTxt", payload=vcTxt)
    with open("vcRole.json", "r") as f:
        vcRole = json.load(f)
        libyuki.push_guilddb(id="vcRole", payload=vcRole)
except:
    traceback.print_exc()

# print(libyuki.get_guilddb_as_dict("txtMsg"))