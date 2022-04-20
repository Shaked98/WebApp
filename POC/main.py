import requests
import logic as engine


def main():
    movie_names = ["Harry Potter and the Sorcerer's Stone",
                   "Harry Potter and the Half-Blood Prince",
                   "Dragon Ball Z: Resurrection 'F'"]

    # add
    for movie in movie_names:
        print("Adding {0} poster to DB".format(movie))
        engine.save_poster(movie)

    # update
    new_movie_name = "Harry Potter and the Deathly Hallows: Part 1"
    print("Replacing {0} poster with {1}".format(movie_names[2], new_movie_name))
    engine.replace_movie(movie_names[2], new_movie_name)

    # delete
    print("Deleting {0} poster from DB".format(new_movie_name))
    engine.delete_poster(new_movie_name)

    # retrieve
    print("movie {0} poster image at {1}".format(new_movie_name, engine.get_poster_location(movie_names[0])))


if __name__ == '__main__':
    main()
