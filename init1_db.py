from google.cloud import firestore


db = firestore.Client()
guilddbRef = db.collection('994483180927201400').document('settings')

# print(str(guilddbRef.get().to_dict()))

# print(str(guilddbRef.get().to_dict()))
var1 = guilddbRef.get().to_dict()

# print(var1['note_channels'])
var1['note_channels']['''1011555656014250014'''] = '''●当サーバーではリアルでの出会いは禁止されてます（身バレ等事件性がありますので。）
●外部ツールの繋がり等の話題もできる限り避けましょう。
●自己防衛やマナーなどに関しては百科事典のガイドラインをご確認ください。
＊リアル等で会う発言をされた人や規約違反者は質問＆報告で通報する事。'''

# print(var1)

print(guilddbRef.update(var1))