import inspect

class Base:
    def get_details(self):
        print(self.__dict__)

    def generate_id(self):
        attributes = self.__dict__.values()
        print(attributes)
        self.inspect_instance()

    def inspect_instance(self):
        pass
