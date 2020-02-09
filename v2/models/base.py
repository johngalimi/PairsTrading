class Base:
    def get_details(self):
        print(self.__dict__)

    def generate_id(self):
        attributes = self.__dict__.values()
        print(attributes)
