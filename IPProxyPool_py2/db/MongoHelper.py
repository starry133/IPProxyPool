import pymongo
from config import DB_CONFIG

from db.ISqlHelper import ISqlHelper


class MongoHelper(ISqlHelper):

    def __init__(self):
        self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'], connect=False)

    def init_db(self):
        self.db = self.client.proxy
        self.proxys = self.db.proxys


    def drop_db(self):
        self.client.drop_database(self.db)


    def insert(self,value=None):
      if value:
          proxy = dict(ip=value['ip'],port=value['port'],types=value['types'],protocol=value['protocol'],country = value['country'],
                       area=value['area'],speed=value['speed'],sites=value['sites'],score=0)
          self.proxys.insert(proxy)



    def delete(self, conditions=None):
        if conditions:
            self.proxys.remove(conditions)
            return ('deleteNum','ok')
        else:
            return ('deleteNum','None')


    def update(self, conditions=None,value=None):
        # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
        if conditions and value:
            self.proxys.update(conditions,{"$set":value})
            return {'updateNum':'ok'}
        else:
            return {'updateNum':'fail'}

    def select(self, count=None,conditions=None):
        if count:
            count = int(count)
        else:
            count=0
        items =self.proxys.find(filter = conditions,limit = count).sort([("speed",pymongo.ASCENDING),("score",pymongo.DESCENDING)])
        results = []
        for item in items:
            result = (item['ip'],item['port'],item['score'])
            results.append(result)
        return results



