from generic_actor import GenericKafkaActor


class ExpenseAnalyticsActor(GenericKafkaActor):
    def __init__(self, message):
        self.message = message

    def process(self, data):
        pass

    def output(self):
        pass




