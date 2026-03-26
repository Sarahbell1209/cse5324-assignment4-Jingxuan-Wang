from payment_strategy import VisaPayment, MastercardPayment, AmexPayment


class PaymentFactory:
    @staticmethod
    def get_payment(card_type):
        if card_type == "visa":
            return VisaPayment()
        elif card_type == "mastercard":
            return MastercardPayment()
        elif card_type == "amex":
            return AmexPayment()
        else:
            raise ValueError("Unsupported card type")