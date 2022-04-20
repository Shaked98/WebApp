from pymongo import MongoClient
import gridfs


def mongo_conn():
    try:
        conn = MongoClient(host='127.0.0.1', port=27017)
        print("MongoDB connected", conn)
        return conn.grid_file

    except Exception as e:
        print("Error in mongo connection:", e)


# upload to mongo from local machine
# receives path including file name
def upload_to_mongo(file_location, name):
    db = mongo_conn()
    file_data = open(file_location, "rb")
    data = file_data.read()
    fs = gridfs.GridFS(db)
    fs.put(data, filename=name)
    print("upload complete")


# download to local machine from mongo
# receives path including file name
def download_from_mongo(download_location, name):
    db = mongo_conn()
    data = db.fs.files.find_one({'filename': name})
    my_id = data['_id']
    fs = gridfs.GridFS(db)
    outputdata = fs.get(my_id).read()
    output = open(download_location, "wb")
    output.write(outputdata)
    output.close()
    print("download complete")
