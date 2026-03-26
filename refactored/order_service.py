class OrderService:
    def __init__(self, db):
        self.db = db

    def create_order(self, user_id, total):
        query = "INSERT INTO orders (user_id, total) VALUES (?, ?)"
        return self.db.execute(query, (user_id, total))