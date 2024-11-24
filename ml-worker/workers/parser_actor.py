from interfaces.generic_actor import GenericKafkaActor
from lib.dalerai.parser import implement_qr



class ParserAnalyticsActor(GenericKafkaActor):
    def __init__(self):
        self.result = None
    @staticmethod
    def __save_img(image: str):
        with open('qr.png', 'wb') as f:
            f.writelines(image)




    def process(self, message):
        image = message.values().decode('utf-8')

        self.__save_img(image)

        self.result = implement_qr(image)


    def output(self):
        return self.result




