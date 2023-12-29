import json

from models  import ClinicAdminSingleton

# Usage
admin1 = ClinicAdminSingleton("admin1", "password1")


# Store the admin objects in a list
admin_list = [admin1.__dict__]

# Write the list to a JSON file
with open("admin_credentials.json", "w") as json_file:
    json.dump(admin_list, json_file)
