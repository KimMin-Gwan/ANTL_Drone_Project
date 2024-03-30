
class Parser():
    def __init__(self):
        pass

    def run(self, head:str, list_data:list):
        return_data = ""
        return_data += head
        return_data += " "

        for data in list_data:
            s_data = str(data)
            return_data += s_data
            return_data += " "
        return return_data