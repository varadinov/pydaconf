import re

from pydaconf.utils.dict import get_dict_value
from pydaconf.utils.exceptions import InterpolationException


def has_interpolation_template(value: str) -> bool:
    """Check if a string contains placeholders for interpolation."""

    return bool(re.search(r"{{\s*(.*?)\s*}}", value))

def interpolate_template(value: str, data: dict) -> str:
    """Replace {{ ... }} placeholders with values from the data dictionary."""
    
    def replace_match(match: re.Match) -> str:
        key_path = match.group(1).strip()  # Extract the key path
        match_value = get_dict_value(data, str(key_path))
        if match_value is None:
            raise InterpolationException(f"Interpolation failed for key '{key_path}'")
        
        return str(match_value)

    return re.sub(r"{{\s*(.*?)\s*}}", replace_match, value)