import gridfs
import requests
from pymongo import MongoClient
from main import get_poster_urls


def download_object(urls):
    """ save the images in a binary object named "contents" """
    for nr, url in enumerate(urls):
        r = requests.get(url)
        contents = r.content
        return contents


def mongo_conn():
    try:
        conn = MongoClient(host='127.0.0.1', port=27017)
        print("MongoDB connected", conn)
        return conn.posters

    except Exception as e:
        print("Error in mongo connection:", e)


# connects to database "posters"
db = mongo_conn()


# download image from imdb straight into mongo
# takes movie_id as 'str' e.g: 'tt4154796'
def download_to_mongo(movie_id):
    urls = get_poster_urls(movie_id)
    data = download_object(urls)
    fs = gridfs.GridFS(db)
    fs.put(data, filename=movie_id)
    print("upload complete")


# first parameter is the download location including the name extension
# second parameter is the file name to search in mongo
def download_from_mongo(download_location, name):
    data = db.fs.files.find_one({'filename': name})
    my_id = data['_id']
    fs = gridfs.GridFS(db)
    outputdata = fs.get(my_id).read()
    output = open(download_location, "wb")
    output.write(outputdata)
    output.close()
    print("download complete")

# testing ground
# download_to_mongo('tt4154796')
# download_to_mongo('tt2395427')
# download_to_mongo('tt4154756')
# download_from_mongo("./pics/tt4154796.jpeg", "tt4154796")
# download_from_mongo("./pics/testing.jpeg", "tt2395427")
