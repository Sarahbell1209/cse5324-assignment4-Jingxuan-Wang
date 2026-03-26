class ProductRepository:
    def __init__(self, db):
        self.db = db

    def find_by_id(self, product_id):
        query = "SELECT * FROM products WHERE id = ?"
        result = self.db.execute(query, (product_id,))
        return result

    def update_stock(self, product_id, new_stock):
        query = "UPDATE products SET stock = ? WHERE id = ?"
        self.db.execute(query, (new_stock, product_id))