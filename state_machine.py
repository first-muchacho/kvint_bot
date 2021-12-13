from transitions import Machine


class CheeseBot(object):  # класс стейт-машины, где хранятся состояния и переходы
    states = ['chilling', 'size_choose', 'payment_method', 'confirmation']

    def __init__(self):
        self.size = None
        self.payment = None

        self.machine = Machine(model=self, states=CheeseBot.states, initial='chilling')

        self.machine.add_transition(trigger='start', source='chilling', dest='size_choose')
        self.machine.add_transition(trigger='pay', source='size_choose', dest='payment_method')
        self.machine.add_transition(trigger='confirm', source='payment_method', dest='confirmation')
        self.machine.add_transition(trigger='done', source='confirmation', dest='chilling')
        self.machine.add_transition(trigger='stop', source='*', dest='chilling')
        self.machine.add_transition(trigger='help', source='*', dest='chilling')

    def set_size(self, size_choose):
        self.size = size_choose
        return self.size

    def set_payment(self, payment_method):
        self.payment = payment_method
        return self.payment
