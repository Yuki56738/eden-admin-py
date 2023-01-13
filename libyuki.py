import json
import traceback
# from google.cloud import data
# from google.cloud.datastore_v1 import *
# from google.cloud.datastore_admin_v1 import *
# from google.cloud.firestore import *

from google.cloud import firestore
from google.cloud.firestore import *

# from google.cloud.firestore_v1 import *
# db = Client
# guilddb = DocumentSnapshot


# def prepare_db():
    # global db
    # global guilddb
    # project_id = "firstproj-36?7213"
def get_db():
    db: Client = firestore.Client()
    return db
def get_guilddb():
    guilddb = get_db().collection("guilddb")
    return guilddb
    # guilddb1: list = guilddb.get()


# x: DocumentSnapshot
# for x in guilddb1:
#     print(x.to_dict())

def push_guilddb(id: str, payload: dict):
    db = get_db()
    guilddb = get_guilddb()
    # with open(jsonFileName, "r") as f:
    # print(json.load(f))
    # guildsettin
    # guilddb.document(document_id=id).create(document_data=json.load(f))

    if not guilddb.document(document_id=id).get().exists:
        guilddb.document(document_id=id).create(document_data=payload)
    else:
        guilddb.document(document_id=id).update(payload)
    # guilddb.add(json.load(f), document_id="guildsettings")

    return guilddb.stream()

# prepare_db()
# add_guildsettings()


def get_guilddb_as_dict(id: str):
    guilddb = get_guilddb()
    return guilddb.document(document_id=id).get().to_dict()



# print(get_guildsettings())
# add_default_guildsettings()
# def get_guildsettings_from_firestore():
# add_default_guildsettings()
# add_default_guildsettings()
# def delete_guildsettings():
#     guilddb_ref = guilddb.get()
# print(guilddb_ref)
# x: DocumentSnapshot
# for x in guilddb_ref:
# print(x.id)
# db.collection("guilddb").recursive()
# delete_guildsettings()

# print(db.get_all(references=CollectionReference("guilddb")))
# var = guilddb1.reference[0]
# print(guilddb1[0].id)
# print(var)

# print(guilddb1[0])

# print(guilddb1[0].to_dict())
# x: DocumentSnapshot
# for x in guilddb1:
# print(x)
# print(x)x
# print(x.to_dic?t())
# print(guilddb1.to_dict())
# print(guil/ddb1)
# print(list(guilddb))

# print()
# guilddb["1234"]
# trans = Transaction()

# guilddb.add(document_data={
#     '2345': '3456'
# }, document_id='1234')
#
# guilddb.stream(transaction=trans)
# guilddb_ref = guilddb.document("guilddb")
# trans = db.transaction()

# guilddb = guilddb_ref.get(tra
# nsaction=trans)
# guilddb1 = guilddb_ref.get

# guilddb1 = guilddb_ref.get(transaction=trans)
# guilddb_ref.get("1234")
# trans.set(reference=guilddb,document_data=guilddb)

# guilddb.stream(transaction=trans)


# guildsettings ={}
#
# guildsettings["guildIdHere"] = "guild-name-here"
# guildsettings["guildIdHero"]["notify_channel_id"] = "notify_channel_name"
#
#
# guilddb["guildidhere"] = 'guild-name-here'
# guilddb["guildidhere"] = 'notify-channnel-id-here'

# transaction = Transaction.create(db, guildsetting)

# db.transaction(firestore.Transaction.commit())


# guilddb.add(guildsettings)
# db.transaction(Client, guilddb)

# db1 = db.collection()
#
#
# class cls1:
#     def key(self, key: str):
#         return "defaultKey"
#
#     def value(self, value: str):
#         return "defaultValue"
#
#
# cls1A = cls1()
#
# cls1A.key("Key1")
# cls1A.value("Value1")
#
# db1.add(document_data=cls1A, document_id="cls1A",)
#

# def create_client():
#     return DatastoreClient()
#

# var1 = create_client()
# #
# # # try:
# print(var1.lookup(project_id=project_id))
#

# except:
# traceback.format_exc()


# class sets1:
#     def name(self, name: str):
#         return name
#
#     def value(self, value: str):
#         return value


# setsA1 = sets1()
#
# setsA1.name(name="name1")
# setsA1.value(value="value1")


# print(var1.get_operation("Key1"))

# createIndexReqRes = CreateIndexRequest(project_id=project_id)
#
# print(createIndexReqRes)

#
# client = DatastoreClient()
# # print(client.lookup(project_id=project_id,read_options=ReadOptions.ReadConsistency()))
#
# print(client.common_project_path(project=project_id))
# firstproj1 = client.common_project_path(project=project_id)
#
# client2 = DatastoreClient()
#
# # print(client2.begin_transaction(project_id=firstproj1))
#
# try:
#     print(client2.list_operations())
# except:
#     traceback.print_exc()
#
# client3 = DatastoreClient()
