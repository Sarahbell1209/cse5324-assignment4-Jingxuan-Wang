class ShoppingCart:
    def __init__(self):
        self.items = []
        self.db = Database()
        self.email_service = EmailService()

    def add_item(self, product_id, quantity, user_id):
        # Check if product exists
        product = self.db.execute_query(
            "SELECT * FROM products WHERE id = " + str(product_id)
        )

        if product:
            # Check stock
            if product['stock'] >= quantity:
                # Calculate price
                if user_id in [1, 5, 10, 23]:  # VIP users
                    price = product['price'] * 0.8
                elif quantity > 10:
                    price = product['price'] * 0.9
                else:
                    price = product['price']

                total = price * quantity

                # Add to cart
                item = {
                    'product_id': product_id,
                    'name': product['name'],
                    'quantity': quantity,
                    'price': price,
                    'total': total
                }
                self.items.append(item)

                # Update stock
                new_stock = product['stock'] - quantity
                self.db.execute_query(
                    "UPDATE products SET stock = " + str(new_stock) +
                    " WHERE id = " + str(product_id)
                )

                # Send notification
                user = self.db.execute_query(
                    "SELECT email FROM users WHERE id = " + str(user_id)
                )
                self.email_service.send_email(
                    user['email'],
                    "Item Added",
                    "You added " + product['name'] + " to your cart"
                )

                return True
            else:
                return False
        else:
            return False

    def calculate_total(self, user_id, promo_code):
        total = 0
        for item in self.items:
            total = total + item['total']

        # Apply discount
        if promo_code == "SAVE10":
            total = total * 0.9
        elif promo_code == "SAVE20":
            total = total * 0.8
        elif promo_code == "SAVE30":
            total = total * 0.7

        # Apply tax
        total = total * 1.0825

        # Shipping
        if total < 50:
            total = total + 10

        return total

    def checkout(self, user_id, payment_info):
        total = self.calculate_total(user_id, payment_info['promo_code'])

        # Process payment
        if payment_info['card_type'] == 'visa':
            # Visa processing
            result = self.process_visa(payment_info['card_number'], total)
        elif payment_info['card_type'] == 'mastercard':
            # Mastercard processing
            result = self.process_mastercard(payment_info['card_number'], total)
        elif payment_info['card_type'] == 'amex':
            # Amex processing
            result = self.process_amex(payment_info['card_number'], total)

        if result:
            # Create order
            order_id = self.db.execute_query(
                "INSERT INTO orders (user_id, total) VALUES (" +
                str(user_id) + ", " + str(total) + ")"
            )

            # Send confirmation email
            user = self.db.execute_query(
                "SELECT email, name FROM users WHERE id = " + str(user_id)
            )
            self.email_service.send_email(
                user['email'],
                "Order Confirmation",
                "Dear " + user['name'] + ", your order #" +
                str(order_id) + " for $" + str(total) + " is confirmed."
            )

            # Clear cart
            self.items = []

            return order_id
        else:
            return None