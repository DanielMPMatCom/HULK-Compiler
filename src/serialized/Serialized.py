import dill

class Serialized:
    def __init__(self) -> None:
        pass

    def save_object(object, object_name):
        with open("object_name", "wb") as file_pkl:
            dill.dump(object, object_name)

    def load_object(object_name):
        with open("object_name", "rb") as file_pkl:
            return dill.load(object_name)
