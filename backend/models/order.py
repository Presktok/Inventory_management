from config.database import mongo

class Order:
    @staticmethod
    def create_order(order_data):
        return mongo.db.orders.insert_one(order_data)


    @staticmethod
    def get_orders():
        return list(mongo.db.orders.find())