from storage_json import StorageJson
from movie_app import MovieApp
from storage_csv import StorageCsv
from argparse import ArgumentParser, Namespace

#creating cli commands line arguments for user to choose its file extension
parser = ArgumentParser()
#creating a variable for user to choose its file type
parser.add_argument('user_choice', help = 'user choice for its file extenstion')
args: Namespace = parser.parse_args()
#splitting up file and name 
user = args.user_choice.split('.')
if user[1] == 'json':
  storage = StorageJson(f'movies.{user[1]}')
elif user[1] == 'csv':
  storage = StorageCsv(f'movies.{user[1]}')
else:
  print(f'{args.user_choice} file extenstion not available')

movie_app = MovieApp(storage)
movie_app.run()
