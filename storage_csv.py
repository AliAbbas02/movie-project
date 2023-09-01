from istorage import IStorage
import csv 

class StorageCsv(IStorage):
  def __init__(self, file_path):
    self.file_path = file_path
   
  def list_movies(self):
    with open(self.file_path) as file:
      csv_movie_reader = csv.DictReader(file)
      all_movies = {'movies':{}}
      for each_movie in csv_movie_reader:
        title = each_movie['title']
        rating = each_movie['rating']
        poster = each_movie['img_url']
        year = each_movie['year']
        imdbID = each_movie["imdbID"]
        country = each_movie['country']
        all_movies['movies'][title] ={'rating' : rating, 'year': year, 'img_url': poster, 'imdbID': title, 'country': country}

      return all_movies

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
    data = data['movies']
    field_names = set(key for outer_key, inner_dict in data.items() for key in inner_dict.keys())
    field_names.add('title')
    with open(file_path , 'w', newline='') as file:
        csv_dict_writer = csv.DictWriter(file, fieldnames=field_names)
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows({**inner_dict, 'title': outer_key} for outer_key, inner_dict in data.items())

        

