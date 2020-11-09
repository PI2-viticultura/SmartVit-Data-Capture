from settings import load_database_params
from extensions import client
import pymongo
import os


class MongoDB():
    def __init__(self):
        if(os.getenv('ENVIRONMENT') != 'developing_local'):
            self.client = client
        else:
            self.params = load_database_params()
            try:
                self.client = pymongo.MongoClient(
                    **self.params,
                    serverSelectionTimeoutMS=10
                )
            except Exception as err:
                print(f'Erro ao conectar no banco de dados: {err}')

    def test_connection(self):
        try:
            self.client.server_info()
            return True
        except Exception as err:
            print(f'Erro ao conectar no banco de dados: {err}')
            return False

    def close_connection(self):
        self.client.close()

    def get_collection(self, collection):
        db = self.client[os.getenv("DBNAME", "smart-dev")]
        collection = db[collection]
        return collection

    def insert_one(self, body, collection):
        try:
            collection = self.get_collection(collection)
            return collection.insert_one(body)

        except Exception as err:
            print(f'Erro ao inserir no banco de dados: {err}')
            return False

    def update_one(self, body, collection):
        try:
            collection = self.get_collection(collection)
            collection.find_one_and_update(
                {"_id": body["_id"]},
                {"$set": body}
            )
            return True

        except Exception as err:
            print(f'Erro ao atualizar no banco de dados: {err}')
            return False

    def delete_one(self, identifier, collection):
        try:
            collection = self.get_collection(collection)
            res = collection.delete_one({"id": identifier})
            if res.deleted_count == 1:
                print(f'Objeto {identifier} removido com sucesso')
            else:
                print(f'Erro ao remover o objeto {identifier}:'
                      ' nenhum objeto com este id encontrado em' + collection)
        except Exception as err:
            print(f'Erro ao deletar no banco de dados: {err}')

    def get_one(self, identifier, collection):
        collection = self.get_collection(collection)
        document = collection.find_one({"_id": identifier})
        return document

    def get_one_by_query(self, query, collection):
        collection = self.get_collection(collection)
        document = collection.find_one(query)
        return document

    def get_one_by_label(self, label, identifier, collection):
        collection = self.get_collection(collection)
        document = collection.find_one({label: identifier})
        return document

    def get_one_by_identifier(self, identifier, collection):
        collection = self.get_collection(collection)
        document = collection.find_one({'identifier': identifier})
        return document

    def get_all(self, collection):
        collection = self.get_collection(collection)
        document = collection.find()
        return document

    def get_winery_by_system_id(self, identifier):
        collection = self.get_collection('winery')
        return collection.find_one({"system._id": identifier})

    def get_system_by_sensor_id(self, identifier):
        collection = self.get_collection('system')
        return collection.find_one({"sensors._id": identifier})
