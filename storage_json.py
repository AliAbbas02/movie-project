from istorage import IStorage
import json

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data. 
        """
        with open(self.file_path) as fileobj:
            movies = json.loads(fileobj.read())
        return movies

    def add_movie(self, title, year, rating, poster, link, country):
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        all_movies = self.list_movies()
        all_movies['movies'][title] = {'rating' : rating, 'year': year, 'img_url': poster, 'imdbID': title, 'country': country}
        self.serialize_data(all_movies, self.file_path)

    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        all_movies = self.list_movies()
        #if movie not in the database
        if not all_movies['movies'][title]:
            raise KeyError
        del all_movies['movies'][title]  
        self.serialize_data(all_movies, self.file_path)

    def update_movie(self, title, notes):
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        all_movies: dict = self.list_movies()
        if not all_movies['movies'][title]:
            raise KeyError 
        all_movies['movies'][title]['rating']: float = notes
        self.serialize_data(all_movies, self.file_path)

    def serialize_data(self, data, file_path):
        'a function that stores data into json file'
        with open(file_path, 'w') as fileobj:
            fileobj.write(json.dumps(data))