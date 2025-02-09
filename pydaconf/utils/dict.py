

def get_dict_value(data: dict, key_path: str) -> str | None | dict:
    keys = key_path.split('.')
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    
    return data
