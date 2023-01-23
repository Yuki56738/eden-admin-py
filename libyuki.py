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
    # tglddoc = thisguildCol_ref.document(document_id="ticket_channel")
    # var3 = tglddoc.get().to_dict()
    var1 = thisguildCol_ref.document(document_id=id)
    # var1 = thisguildCol_ref.get()
    return var1.get().to_dict()

def get_guildsettings2_as_dict(id: str):
    db = Client()
    guilddbcol = db.collection('guilddb')
    guildsettingsDoc = guilddbcol.document('guildsettings')
    guildsettingsCol1:CollectionReference = guildsettingsDoc.collection(id)
    return guildsettingsCol1.document(id).get().to_dict()
def push_to_guildsettings2_from_dict(id: str, payload: dict):
    db = Client()
    guilddbcol = db.collection('guilddb')
    guildsettingsDoc = guilddbcol.document('guildsettings')
    guildsettingsCol1: CollectionReference = guildsettingsDoc.collection(id)
    try:
        guildsettingsCol1.document(id).update(payload)
    except:
        guildsettingsCol1.document(id).create(payload)
    # return guildsettingsCol1.document(id).get().to_dict()
def push_ticketdb(id:str, payload:dict):
    return push_to_guildsettings2_from_dict(id=id, payload=payload)
    # db = firestore.Client()
    # guilddbCol = db.collection("guilddb")
    # guildsettingsDoc_ref = guilddbCol.document("guildsettings")
    # thisguildCol_ref: CollectionReference = guildsettingsDoc_ref.collection(str(id))
    # # tglddoc = thisguildCol_ref.document(document_id="ticket_channel")
    # glclog = thisguildCol_ref.document(document_id=id)
    # return glclog.update(payload)


# print(get_guildsettings2_as_dict('994483180927201400'))

# print(push_to_guildsettings2_from_dict(id='1234', payload={
#     'id': '1234',
#     'name': 'naeiogfahio'
# }))
#
# print(get_guildsettings2_as_dict('1234'))

# print()