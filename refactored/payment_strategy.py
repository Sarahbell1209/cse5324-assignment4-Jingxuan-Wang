from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount, card_number):
        pass


class VisaPayment(PaymentStrategy):
    def pay(self, amount, card_number):
        return True


class MastercardPayment(PaymentStrategy):
    def pay(self, amount, card_number):
        return True


class AmexPayment(PaymentStrategy):
    def pay(self, amount, card_number):
        return True