from csv import DictReader
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import (
    Title,
    Category,
    Genre,
    Review,
    GenreTitle,
    Comment)

User = get_user_model()


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the reviews data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Показать это, когда пользователь наберет help    
    help = "Загружает данные из всех csv-файлов для тестирования приложения"
    
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        
    def handle(self, *args, **kwargs):
        path = kwargs['path']
        filepath='/'.join([path, 'category.csv'])
        self.load_category_data(filepath='/'.join([path, 'category.csv']))
        self.load_genre_data(filepath='/'.join([path, 'genre.csv']))
        self.load_titles_data(filepath='/'.join([path, 'titles.csv']))
        self.load_genre_title_data(filepath='/'.join([path, 'genre_title.csv']))
        self.load_users_data(filepath='/'.join([path, 'users.csv']))
        self.load_review_data(filepath='/'.join([path, 'review.csv']))
        self.load_comment_data(filepath='/'.join([path, 'comments.csv']))


    def load_category_data(self, filepath):
        # Показать это сообщение, если данные уже есть в БД        
        if Category.objects.exists():
            print('Данные по категориям уже загружены...выходим.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Показываем это сообщение перед началом загрузки данных в БД
        print("Загружаем данные по категориям")

        #Загружаем данные в БД
        bulk_list = list()
        for row in DictReader(open(filepath, encoding="utf-8-sig")):
            category=Category(id=row['id'], name=row['name'], slug=row['slug'])  
            bulk_list.append(category)
        Category.objects.bulk_create(bulk_list)

    def load_genre_data(self, filepath):
        if Genre.objects.exists():
            print('Данные по жанрам уже загружены...выходим.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        
        print("Загружаем данные по жанрам")
        
        bulk_list = list()
        for row in DictReader(open(filepath, encoding="utf-8-sig")):
            genre=Genre(id=row['id'], name=row['name'], slug=row['slug'])  
            bulk_list.append(genre)
        Genre.objects.bulk_create(bulk_list)

    def load_titles_data(self, filepath):
        if Title.objects.exists():
            print('Данные по произведениям уже загружены...выходим.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        print("Загружаем данные по произведениям")

        bulk_list = list()
        for row in DictReader(open(filepath, encoding="utf-8-sig")):
            title=Title(id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category_id=row['category'])  
            bulk_list.append(title)
        Title.objects.bulk_create(bulk_list)

    def load_genre_title_data(self, filepath):
        if GenreTitle.objects.exists():
            print('Данные по связи жанров и произведений уже загружены...выходим.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        
        print("Загружаем данные по связи жанров и произведений")

        bulk_list = list()
        for row in DictReader(open(filepath, encoding="utf-8-sig")):
            renre_title=GenreTitle(id=row['id'], title_id=row['title_id'], genre_id=row['genre_id'])  
            bulk_list.append(renre_title)
        GenreTitle.objects.bulk_create(bulk_list)
   
    def load_users_data(self, filepath):
        if User.objects.exists():
            print('Данные по пользователям уже загружены...выходим.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        print("Загружаем данные по пользователям")

        bulk_list = list()
        for row in DictReader(open(filepath, encoding="utf-8-sig")):
            user=User(id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'])  
            bulk_list.append(user)
        User.objects.bulk_create(bulk_list)

    def load_review_data(self, filepath):
        if Review.objects.exists():
            print('Данные по отзывам уже загружены...выходим.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        print("Загружаем данные по отзывам")

        bulk_list = list()
        for row in DictReader(open(filepath, encoding="utf-8-sig")):
            review=Review(id=row['id'],
                        title_id=row['title_id'],
                        text=row['text'],
                        author_id=row['author'],
                        score=row['score'],
                        pub_date=row['pub_date'])  
            bulk_list.append(review)
        Review.objects.bulk_create(bulk_list)

    def load_comment_data(self, filepath):
        if Comment.objects.exists():
            print('Данные по комментариям уже загружены...выходим.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        print("Загружаем данные по комментариям")

        bulk_list = list()
        for row in DictReader(open(filepath, encoding="utf-8-sig")):
            comment=Comment(id=row['id'],
                            review_id=row['review_id'],
                            text=row['text'],
                            author_id=row['author'],
                            pub_date=row['pub_date'])  
            bulk_list.append(comment)
        Comment.objects.bulk_create(bulk_list)

