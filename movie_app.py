import difflib
from random import randrange
import requests
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
from storage_json import StorageJson

class MovieApp:
    def __init__(self, storage):
        self._storage = storage


    def _command_list_movies(self):
        movies = self._storage.list_movies()
        return movies

    def _command_add_movie(self, API_KEY, URL):
        'a function that adds a movie in the database'
        title = input('Enter new movie name: ').title()
        try:
        #if movie already exists
            if self._storage.list_movies()['movies'][title]:
             return f'{title.title()} already exists'
        except KeyError:
            #get the movie from server      
            try:
                response = requests.get(URL, params={'t': title, 'apikey': API_KEY}).json()
                if response['Response'] == 'True':
                    title:str = response['Title']
                    year:int = int(response['Year'])
                    rating:float = float(response['imdbRating'])
                    image_url:str = response['Poster']
                    link:str = response['imdbID'] 
                    country:list = response['Country']
                    #add the movie into database
                    self._storage.add_movie(title, year, rating, image_url, link, country)
                    return f'Movie {title.title()} succesfully added'
                else:
                    return 'movie not found in database'  
            #if cannot connect to server    
            except requests.exceptions.ConnectionError as e:
                return 'connection time out ....\nplease see troubleshoot for help'
    
    def _command_delete_movie(self):
        ' a fucntion that deletes a movie from movie database'
        title = input('enter the movie title you want to delete: ').title()
        try:  
            self._storage.delete_movie(title)
            return 'movie succesfully removed'
        except KeyError:
            return 'movie not found in the database'
        
    def _command_update_movie(self):
        ' a function that updates the rating of a movie'
        title: str = input('enter the movie name: ').title()
        note: str = input('enter movie notes: ')
        try:
            self._storage.update_movie(title, note)
            return 'movie succesfully updated'
        except KeyError:
            return 'movie not in database'
    
    def changed_structure(self):
        ' a function that returns a dict of movies and their ratings only'
        data: dict = self._storage.list_movies()
        return {name: value['rating'] for name, value in data['movies'].items()}
    
    @staticmethod
    def average_rating(movies):
        'a function that returns average rating of all the movies in the database'
        return sum(list(movies.values())) / len(movies)
    
    @staticmethod
    def median(movies):
        'a function that returns meidan'
        ratings = list(sorted(movies.values()))
        if len(ratings) %2 != 0:
            return ratings[(len(ratings) + 1) // 2]
        else:
            return (ratings[len(ratings) // 2] + (ratings[(len(ratings) // 2) + 1]))/2

    @staticmethod
    def best_movie(movies):
        'a function that returns movies with the highest ratings'
        max_rating = max(movies.values())
        return [(movie,rating) for movie,rating in movies.items() if rating == max_rating ]  
    
    @staticmethod
    def worst_movie(movies):
        ' a function that returns movies with he lowest ratings'
        min_rating = min(movies.values())
        return [(movie,rating) for movie,rating in movies.items() if rating == min_rating ] 

    
    def _command_stats(self):
        ' a function that prints stats for movie database'
        #average ratings for the a movie
        print(f'Average rating: {self.average_rating(self.changed_structure()):.2f}')
        #median ratings for all the movies in the database
        #print(f'Median rating: {self.median(self.changed_structure())}')
        #best movie with the top rating
        for movie,rating in self.best_movie(self.changed_structure()):
            print(f'Best Movie: {movie}, {rating}')
        #movie with the lowest rating
        for movie,rating in self.worst_movie(self.changed_structure()):
            ' a function that returns movies with the lowest rating'
            print(f'Worst Movie: {movie}, {rating}')

    def _command_random_movie(self):
        ' a function that returns a random movie from a database'
        random = randrange(len(self.changed_structure()))
        random_movie = list(self.changed_structure().items())[random]
        return random_movie

    def _command_search_movie(self, movie_to_search):
        ' a function that returns, if movie is in the database'
        # if searched movie matched the key fully
        movie_list = [movie.lower() for movie in self.changed_structure().keys()]
        check=[True for movie in movie_list if movie_to_search == movie]
        if len(check) >= 1:
            return [(movie,rating) for movie,rating in self.changed_structure().items()\
                    if movie_to_search.lower() in movie.lower()]
        #if a typo but some of it matched
        elif len(check) == 0:
            words_to_search = movie_to_search.lower().split()
            movie_listt = [(movie,rating) for movie,rating in self.changed_structure().items()\
                    if any(difflib.get_close_matches(word, movie.lower().split(), n=1, cutoff=0.8)\
                        for word in words_to_search)]
            if len(movie_listt) >= 1:
                print(f'movie not found by that name...\n'
                f'are you looking for this movie......')
                return movie_listt
            else:
                check=[True for movie in movie_list if movie_to_search in movie]
                if len(check)>=1:
                    print(f'movie not found by that name...\n'
                    f'are you looking for this movie......')
                    return [(movie,rating) for movie,rating in self.changed_structure().items()\
                        if movie_to_search.lower() in movie.lower()] 
        

    def _command_movies_sorted_by_rating(self):
          'a fucntion that returns a dictionary of sorted by values in descending'
          return dict(sorted(self.changed_structure().items(), key=lambda item: item[1], reverse=True ))


    def _commnad_create_histogram(self):
        'a function that creates and saves a histogram of our database'
        data = list(sorted(self.changed_structure().values()))
        bins = 10
        plt.title('Movie ratings')
        plt.xlabel('ratings')
        plt.ylabel('total movies in rating')
        plt.hist(data,bins=bins,edgecolor='black')  
        print('Histogram created')
        s = input('would you like to save histogram in a file, press s for save or enter to continue: ')
        if s =='s':
            filename = input('please enter the file name in which you would like to save the histogram: ')
            plt.savefig(f'{filename}.jpeg')
            print('histogram saved')
            plt.show()  
    
    def generate_html_code(self, data: dict)->str:
        'a function that converts each data into html code'
        html = ''
        for movie, details in data.items():
            html += '<li>'
            html += '<div class= "movie tooltip">'
            #if any movie has notes add extra html 
            if 'movie_notes' in details.keys():
                html += '<span class="tooltip-text">{}</span>'.format(details['movie_notes'])
            html += '<a href="https://www.imdb.com/title/{}/">'.format(details['imdbID'])
            html += '''<img class= "movie-poster\" src={} alt=\'a movie picture\'"></a>
            <p class= "movie-title">{}</p>
            <p class= "movie-year">{}</p>
            <p class= "rating">{}{}<span>{}</span></p>
            </div>
            </li>
            '''.format(details['img_url'], movie, details['year'], (int(float(details['rating'])//2))*'*',\
            details['rating'],self.country_codes_flags(details['country']) )
        return html
    
    @staticmethod
    def country_codes_flags(countries:list) -> list:
        'a function that gets flag icons'
        #get country code beacuse api uses country codes
        country_codes = requests.get('https://flagcdn.com/en/codes.json').json()
        flags=''
        for code,country_name in country_codes.items():
            #make an image tag for each country in list for each movie
            if country_name in countries:
             flags += "<img src= 'https://flagcdn.com/16x12/{}.png' alt = 'flag'/>".format(code)
        return flags
    
    def _command_generate_website(self, file):
        'a function that adds data converted html into html file'
        with open(file) as html_file:
            html:str = html_file.read().strip()
        soup = BeautifulSoup(html, 'html.parser')
        #parsing title and changing its text
        title = soup.find('h1')
        title.string = 'MasterSchool Movie-App'
        movie_data = self._storage.list_movies()['movies']
        ol_tag = soup.find('ol')
        #return a string of html_code
        html_updated_code = self.generate_html_code(movie_data)
        new_soup = BeautifulSoup(html_updated_code, 'html.parser')
        li_tags = new_soup.find_all('li')
        #create a new ol tag and append all li tags 
        new_ol_tag = new_soup.new_tag('ol')
        #copy the class attribute of old ol to new ol 
        new_ol_tag.attrs['class'] = ol_tag.attrs['class']
        for each_li in li_tags:
            new_ol_tag.append(each_li)
        ol_tag.replace_with(new_ol_tag)
        return soup.prettify()

    def run(self):
        'main function'
        API_KEY: str = 'd322e1a0'
        URL: str = 'http://www.omdbapi.com/'
        #absoulute file path for html file
        html_file_path = 'staticc/index_template.html' 
        while True:
            print('*'*10,' My Movies Database ','*'*10,'\n')
            print((f'Menu:\n'
                f'0. Exit\n'
                f'1. list movies\n'
                f'2. Add movie\n'
                f'3. Delete movie\n'
                f'4. Update movie\n'
                f'5. Stats\n'
                f'6. Random movie\n'
                f'7. Search movie\n'                       
                f'8. Movies sorted by rating\n'
                f'9. Create ratings histogram\n'
                f'10.Generate_website\n\n'))
            #user input functionality
            try:      
                user_choice = int(input('Enter Choice (1-10): '))
                if user_choice in range(1, 11):
                    self.all_function(user_choice, html_file_path, API_KEY, URL)
                    input('\nPress Enter/key(any) To Continue ')
                elif user_choice == 0:
                    self.all_function(user_choice)
                    break
                else:
                    print('option not in the list please try again')  
            except ValueError:
                print('please select an option from the list')

    def all_function(self, choice, html_file:str = '', API_KEY:str = '', URL: str = ''):
        'a functions that has all the functions for the app'
        if choice == 1:
            all_movies = self._storage.list_movies()
            if all_movies['movies'] != {}:
                for movie, values in all_movies['movies'].items():
                  print(f'{movie} {values["year"]}')
            else:
                print('sorry no movie in database')    
        elif choice== 2:
            print(self._command_add_movie(API_KEY, URL))
        elif choice== 3:
            print(self._command_delete_movie())
        elif choice== 4:
            print(self._command_update_movie())
            # data = self._command_generate_website(html_file)


            # with open(html_file, 'w') as fileobj:
            #     fileobj.write(data)
            # print('website updated succesfully')
        elif choice== 5:
            self._command_stats()
        elif choice== 6:
            movie,rating=self._command_random_movie()
            print(movie,' it\'s rated ',rating)
        elif choice== 7:
            search=input('Enter movie to search: ')
            check=self._command_search_movie(search)
            if check != None:
                for movie,rating in check:
                    print(movie,' ',rating)
            else:
                print('movie not found')
        elif choice== 8:
            for movie,rating in self._command_movies_sorted_by_rating().items():
                print(movie,' ',rating)
        elif choice == 9:
            self._commnad_create_histogram()
        elif choice == 10:
            data = self._command_generate_website(html_file)
            with open(html_file, 'w') as fileobj:
                fileobj.write(data)
            print('website generated succesfully')
        elif choice == 0:
            print('Bye!')


if __name__ == "__main__":
    storage = StorageJson('movies.json')
    movie_app = MovieApp(storage)
    movie_app.run()

