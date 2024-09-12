import yaml

def load_yaml(file_path):
    """
    Load a YAML configuration file and return its contents as a dictionary.
    
    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: A dictionary representation of the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

