from flask import Flask, redirect, url_for, render_template, request, json, Response
import imdb, os
import requests
from config import KEY
from pymongo import MongoClient

app = Flask(__name__)

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'


def _get_json(url):
    r = requests.get(url)
    return r.json()


def _download_images(urls, path='.'):
    """download all images in list 'urls' to 'path' """

    for nr, url in enumerate(urls):
        r = requests.get(url)
        filetype = r.headers['content-type'].split('/')[-1]
        filename = 'poster_{0}.{1}'.format(nr + 1, filetype)
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
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url)

    return poster_urls


def tmdb_posters(imdbid, count=None, outpath='.'):
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
    search = ia.search_movie(movie)

    if request.method == "POST":
        pass

    return render_template("search.html", content=search)


@app.route('/search', methods=["GET", "POST"])
def download():
    # takes ID of first Movie found.
    movie_id = "tt" + search[0].movieID
    tmdb_posters(movie_id)

if __name__ == "__main__":
    app.run()
