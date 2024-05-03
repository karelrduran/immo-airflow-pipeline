import os
import json


class SettingsManipulation:
    def __init__(self):
        self.json_file = os.path.join(os.path.dirname(__file__), "settings.json")

    def load_json(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
                if json_data:
                    return json_data
        else:
            self.save_json(json_data={})
        return {}

    def save_json(self, json_data):
        with open(self.json_file, 'w') as f:
            json.dump(json_data, f, indent=4)

    def update_json(self, json_data):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
                if json_data:
                    json_data.update(json_data)
                self.save_json(json_data=json_data)

    def update_last_date(self, last_date):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
                json_data['LAST_UPDATE'] = last_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
                self.save_json(json_data=json_data)


# "LAST_UPDATE": "2024-04-29T00:00:00.000+0000",

# sett_manip = SettingsManipulation()
# print(sett_manip.json_file)
# print(sett_manip.load_json())
# SettingsManipulation.update_last_date(last_date="2024-12-29T00:00:00.000+0000")

