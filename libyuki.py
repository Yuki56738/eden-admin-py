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