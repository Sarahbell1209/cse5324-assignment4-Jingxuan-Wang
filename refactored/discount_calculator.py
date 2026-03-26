class DiscountCalculator:
    def apply_discount(self, total, promo_code):
        if promo_code == "SAVE10":
            return total * 0.9
        elif promo_code == "SAVE20":
            return total * 0.8
        elif promo_code == "SAVE30":
            return total * 0.7
        return total