import json


def list_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 
    """
    with open('data.json') as fileobj:
        movies = json.loads(fileobj.read())
        return movies
        
 
def add_movie(title, year, rating, image_url):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    all_movies = list_movies()
    all_movies['movies'][title] = {'rating' : rating, 'year': year, 'img_url': image_url}
    serialize_data(all_movies, 'data.json')


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    all_movies = list_movies()
    #if movie not in the database
    if not all_movies['movies'][title]:
      raise KeyError
    del all_movies['movies'][title]  
    serialize_data(all_movies, 'data.json')
    

def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    all_movies: dict = list_movies()
    if not all_movies['movies'][title]:
      raise KeyError 
    all_movies['movies'][title]['rating']: float = rating
    serialize_data(all_movies, 'data.json')


def serialize_data(data, file_name):
    'a function that stores data into json file'
    with open(file_name, 'w') as fileobj:
        fileobj.write(json.dumps(data))
