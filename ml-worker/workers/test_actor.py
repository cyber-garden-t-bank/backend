from interfaces.generic_actor import GenericKafkaActor



class TestActor(GenericKafkaActor):
    def __init__(self, message):
        self.message = message
        self.result = None

    def process(self, message):
        self.result = message

    def output(self):
        return self.result




