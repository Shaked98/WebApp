from flask import Flask, redirect, url_for, render_template, request, json, Response
import imdb, os
import requests
from config import KEY
from pymongo import MongoClient
import os.path

app = Flask(__name__)

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'


def _get_json(url):
    r = requests.get(url)
    return r.json()


def _download_images(urls, path='./static'):
    """download all images in list 'urls' to 'path' """

    for nr, url in enumerate(urls):
        r = requests.get(url)
        filetype = r.headers['content-type'].split('/')[-1]
        filename = '{0}_{1}.{2}'.format(movie_id, nr + 1, filetype)
        filepath = os.path.join(path, filename)
        with open(filepath, 'wb') as w:
            w.write(r.content)


def get_poster_urls(imdbid):
    """ return image urls of posters for IMDB id
        returns all poster images from 'themoviedb.org'. Uses the
        maximum available size.
        Args:
            imdbid (str): IMDB id of the movie
        Returns:
            list: list of urls to the images
    """
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """

    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])

    max_size = max(sizes, key=size_str_to_int)

    posters = _get_json(IMG_PATTERN.format(key=KEY, imdbid=imdbid))['posters']
    poster_urls = []
    poster = posters[0]
    rel_path = poster['file_path']
    url = "{0}{1}{2}".format(base_url, max_size, rel_path)
    poster_urls.append(url)

    return poster_urls


def tmdb_posters(imdbid, count=None, outpath='./static'):
    urls = get_poster_urls(imdbid)
    if count is not None:
        urls = urls[:count]
    _download_images(urls, outpath)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/', methods=["POST"])
def search():
    # movie name
    global movie
    movie = request.form['movie']
    return redirect(url_for("results"))


# show the images and results of the search method
@app.route('/search', methods=["GET", "POST"])
def results():
    ia = imdb.IMDb()
    global search
    global my_list
    search = ia.search_movie(movie)
    # my list has the conditions, if true the file exists.
    my_list = []

    # making a list of True/False
    for key in search:
        file_exists = os.path.exists(f'./static/tt{key.movieID}_1.jpeg')
        my_list.append(file_exists)

    global my_zip
    my_zip = list(zip(search, my_list))

    for name, condition in my_zip:
        print("Movie Name:", name)
        print("Movie ID:", name.movieID)
        print("Movie Condition:", condition)
    return render_template("search.html", content=my_zip, condition=my_zip)


@app.route('/search/download', methods=["GET", "POST"])
def download():
    if request.method == 'POST':
        # receive Movie ID list
        download = request.form.getlist('movieID')
        # download all the chosen movies.
        global movie_id
        for movie_id in download:
            tmdb_posters(movie_id)
        return render_template("download.html")


if __name__ == "__main__":
    app.run()
