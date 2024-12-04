import yaml

def load_yaml(file_path):
    with open(file_path, "r") as file:
        print("---------------- SEE HERE -----------")
        print(yaml.safe_load(file))
        return yaml.safe_load(file)
