import local_storage_provider as storage
# import storage_provider as storage
import imdb
import requests
from config import KEY

ia = imdb.IMDb()

# def api_init():
# get the system-wide configuration as json
CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
url = CONFIG_PATTERN.format(key=KEY)
r = requests.get(url)
config = r.json()
# print(config['images'])

# define size of poster + base url for API configuration
base_url = config['images']['base_url']
sizes = config['images']['poster_sizes']
max_size = 'original'
"""
    'sizes' should be sorted in ascending order, so
        max_size = sizes[-1]
    should get the largest size as well.        
"""

# max_size = max(sizes, key=size_str_to_int)



def size_str_to_int(x):
    return float("inf") if x == 'original' else int(x[1:])

def movie_search(name):
    return ia.search_movie(name)


# return IMDB id first movie match or None
def get_movie_id(name):
    res = ia.search_movie(name)

    if res:
        return res[0].movieID
    else:
        return None


def save_poster(movie_name):
    IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
    movie_id = "tt"+get_movie_id(movie_name)
    response = requests.get(IMG_PATTERN.format(key=KEY, imdbid=movie_id)) # for example 'tt0095016'
    response_json = response.json()

    # assembles the image urls and adds them to a list
    posters = response_json['posters']

    # poster_urls = []
    # for poster in posters:
    #     rel_path = poster['file_path']
    #     url = "{0}{1}{2}".format(base_url, max_size, rel_path)
    #     poster_urls.append(url)

    rel_path = posters[0]['file_path']
    url = "{0}{1}{2}".format(base_url, max_size, rel_path)

    storage.write_file(url, movie_id + ".jpg")

# replaces the posters accordingly
def replace_movie(old_movie_name, new_movie_name):
    delete_poster(old_movie_name)
    save_poster(new_movie_name)


def delete_poster(movie_name):
    movie_id = "tt"+get_movie_id(movie_name)
    storage.delete_file(movie_id + ".jpg")

# from our storage
def get_poster_location(movie_name):
    movie_id = "tt" + get_movie_id(movie_name)
    return storage.get_file(movie_id+".jpg")


if __name__ == '__main__':
    # api_init()
    pass