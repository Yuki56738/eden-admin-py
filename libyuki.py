import json
import traceback

from google.cloud import firestore
from google.cloud.firestore import *


def get_db():
    db: Client = firestore.Client()
    return db


def get_guilddb():
    guilddb = get_db().collection("guilddb")
    return guilddb


def push_guilddb(id: str, payload: dict):
    db = get_db()
    guilddb = get_guilddb()

    if not guilddb.document(document_id=id).get().exists:
        guilddb.document(document_id=id).create(document_data=payload)
    else:
        guilddb.document(document_id=id).update(payload)

    return guilddb.stream()


def get_guilddb_as_dict(id: str):
    guilddb = get_guilddb()
    return guilddb.document(document_id=id).get().to_dict()


def get_ref_guilddb(id: str):
    guilddb = get_guilddb()
    return guilddb.document(document_id=id)

def list_guilddb(id: str):
    guilddb_ref = get_ref_guilddb(id)
    return guilddb_ref
def get_ticketdb_as_dict(id:str):
    db = firestore.Client()
    guilddbCol = db.collection("guilddb")
    guildsettingsDoc_ref = guilddbCol.document("guildsettings")
    thisguildCol_ref: CollectionReference = guildsettingsDoc_ref.collection(str(id))
    tglddoc = thisguildCol_ref.document(document_id="ticket_channel")
    var3 = tglddoc.get().to_dict()
    return var3

# list_guilddb()

# var1 = list_guilddb("guildsettings").get()
#


# print(var1.to_dict())

# guilddb_ref = get_ref_guilddb("guildsettinfs")
#
# guilddbs = guilddb_ref.stream()

# guilddb_ref = get_guilddb()
#
# guilddb = guilddb_ref.stream()
#
# for x in guilddb:
#     print(f"{x.id} => {x.to_dict()}")
#     if x.id == ""