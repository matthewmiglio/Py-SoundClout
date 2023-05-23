import pickle
from os import makedirs
from os.path import exists, expandvars, join
from typing import Any

# a module to cache and load program data to and from the disk

module_name = "py-TwitterBot"

top_level = join(expandvars("%appdata%"), module_name)

# Method to cache data to the disk using pickle
def _cache_data(data, file_name) -> None:
    # a method to cache data to the disk using pickle
    file_path = join(top_level, file_name)
    if not exists(top_level):
        makedirs(top_level)
    with open(file_path, "wb") as f:
        pickle.dump(data, f)
    print(f"Cached dat to {file_name}")


# Method to retrieve stored data from the disk using pickle
def _load_data(file_name) -> Any | None:
    # a method to load data from the disk using pickle
    file_path = join(top_level, file_name)
    if not exists(file_path):
        return None
    with open(file_path, "rb") as f:
        try:
            return pickle.load(f)
        except pickle.UnpicklingError:
            return None


# method to cache the user settings to the Py-TwitterBot folder
def cache_user_settings(data: dict[str, Any] | None) -> None:
    # a method to cache user settings to the disk
    _cache_data(data, "user_settings.dat")


# Method to read the user settings from the disk
def read_user_settings() -> dict[str, Any] | None:
    # a method to read user settings from the disk
    return _load_data("user_settings.dat")


# Method to check if the user settings file exists
def check_for_user_settings_file() -> bool:
    # a method to check if the user settings file exists
    return exists(join(top_level, "user_settings.dat"))


# method to check if the program state file exists
def check_for_program_state_file() -> bool:
    return exists(join(top_level, "program_state_data.dat"))


# method to cache the program state to the Py-TwitterBot folder
def cache_program_state(program_state_string):
    _cache_data(program_state_string, "program_state_data.dat")


# method to read the program state from the disk
def read_program_state():
    return _load_data("program_state_data.dat")




def check_user_settings() -> bool:
    # a method to check if the user settings file exists
    return exists(join(top_level, "user_settings.dat"))




# method to make sure the program state file exists
if not check_for_program_state_file():
    print("creating program state file")
    cache_program_state(program_state_string="following")
