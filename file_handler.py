import json


class FileHandler:
    @staticmethod
    def save_data(data):
        with open('section_data.json', 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_data():
        with open('section_data.json', 'r') as f:
            data = json.load(f)
        return data
