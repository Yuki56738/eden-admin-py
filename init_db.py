import discord
from discord import *
from discord.ui import *

from google.cloud.firestore import *
import libyuki

print(libyuki.get_guilddb_as_dict())

print(libyuki.push_guilddb({
    '994483180927201400': {
        'create_vc_channel': 1019948085876629516,
        'member_role': 997644021067415642
    }
}))
print(libyuki.get_guilddb_as_dict())

# print(libyuki.push_guilddb({
#     '1234': '5678'
# }))

# db = Client()
#
# guilddb = db.collection('guilddb')
#
# guildsettings = guilddb.document('guildsettings')
#
# # guildsettingsDoc1 = guildsettings.get().
#
# guildsettingsDoc1 = guildsettings.get().to_dict()
# print(guildsettings)
# print(guildsettingsDoc1)
#
# # guildsettingsDoc1.update({
# #     '994483180927201400': {
# #         'create_vc_channel': '1019948085876629516'
# #     }
# #
# # })
#
# # print(guildsettings.get().to_dict()['994483180927201400'])
#
# guildsettings.update({
#     '994483180927201400': {
#         'create_vc_channel': '1019948085876629516',
#         'member_role': '997644021067415642'
#     }
# })
#
# # guildsettings