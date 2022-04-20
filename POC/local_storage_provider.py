import requests
import os
from pathlib import Path

# saves the file at file_URL as save_as
# if already exists with this name, automatically overwrites
# returns True on success, otherwise False
def write_file(file_URL, save_as):
    # store all posters as poster_1.jpg, poster_2.jgp, etc. in the current directory
    response = requests.get(file_URL)
    if response.status_code != 200:
        return False

    try:
        with open(save_as, 'wb') as writer:
            writer.write(response.content)
    except OSError:
        return False

    return True

# returns full absolute path to file
# if not exists - empty string
def get_file(file_name):
    file_path = Path(file_name).absolute()
    if file_path.exists():
        return str(file_path.absolute())
    else:
        return ""

# deletes the file
def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

# renames file_name with new_file_name
# returns True on success, otherwise False
def rename_file(file_name, new_file_name):
    if os.path.exists(file_name):
        os.rename(file_name, new_file_name)
        return True
    else:
        return False


if __name__ == '__main__':

    file_name = "tt123.jpg"
    new_name = "tt124.jpg"
    file_url = "http://image.tmdb.org/t/p/original/rTDPh94aNYOCDgsS4RGSJJsWLPH.jpg"

    result = write_file(file_url, file_name)
    if not result:
        exit(1)

    result = get_file(file_name)
    if not result.endswith(os.sep + file_name):
        exit(2)

    result = rename_file(file_name, new_name)
    if not result:
        exit(3)

    delete_file(new_name)
    # verify deletion
    result = get_file(file_name)
    if result != "":
        exit(4)
