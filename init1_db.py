from google.cloud import firestore


db = firestore.Client()
guilddbRef = db.collection('994483180927201400').document('settings')

# print(str(guilddbRef.get().to_dict()))

# print(str(guilddbRef.get().to_dict()))
var1 = guilddbRef.get().to_dict()

# print(var1['note_channels'])
var1['note_channels']['''1016234230549843979'''] = '''【名前／年齢 ／性別 】／／ 
【 対象／好み 】例：女性／カワボ／／ 
【属性 】例：S,M、ノーマル、スイッチャー 
【 好きなプレイ 】例：イチャ甘／／ 
【 嫌いなプレイ 】例：バチボコ／／ 
【 寝落ちの可否 】
 【 公開 ／複数 】例：OK／複数は女性のみ 
【ＰＲ】'''

# print(var1)

print(guilddbRef.update(var1))