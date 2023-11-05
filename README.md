## 01.ORM Introduction

- Object-Relational Mapping (ORM) е техника, която позволява на разработчиците да работят с релационни бази данни, използвайки обектно-ориентиран подход.
- ORM позволява взаимодействие с базата данни чрез обекти и класове вместо да се използват SQL заявки.
- Данните се съпоставят между таблиците в базата данни и обекти в Python.
- ORM е съвместим с различни системи за управление на бази данни.
- В Django ORM, моделите се дефинират като Python класове и се използват за създаване, извличане, обновление и изтриване на записи в базата данни.

## 02.Django Models Basics

01.Django models

  - Всеки модел е отделна таблица
  - Всяка променлива използваща поле от models е колона в тази таблица
  - Моделите ни позволяват да не ни се налага писането на low level SQL
    
02.Създаване на модели

  - Наследяваме models.Model
    
03.Migrations

  - makemigrations
  - migrate
    
04.Други команди

  - dbshell - отваря конзола, в коятоо можем да пишем SQL
  - CTRL + ALT + R - отваря manage.py console

## 03.Migrations and Django Admin

01.Django Migrations Advanced
  - Миграциите ни помагат надграждаме промени в нашите модели
  - Както и да можем да пазим предишни стейтове на нашата база
  - Команди:
    - makemigrations
    - migrate
    - Връщане до определена миграция - migrate main_app 0001
    - Връщане на всички миграции - migrate main_app zero
    - showmigrations - показва всички апове и миграциите.
    - showmigrations app_name - показва миграциите за един app
    - showmigrations --list - showmigrations -l
    - squashmigrations app_name migration_to_which_you_want_to_sqash - събира миграциите до определена миграция в една миграция
    - sqlmigrate app_name migration_name - дава ни SQL-а на текущата миграция - използваме го, за да проверим дали миграцията е валидна
    - makemigrations --empty main_app - прави празна миграция в зададен от нас app

02.Custom/Data migrations
  - Когато например добавим ново поле, искаме да го попълним с данни на база на вече съществуващи полета, използваме data migrations
  - RunPython
    - викайки функция през него получаваме достъп до всички апове и техните модели (първи параметър), Scheme Editor (втори параметър)
    - добра практика е да подаваме фунцкия и reverse функция, за да можем да връщаме безпроблемно миграции
  - Scheme Editor - клас, който превръща нашия пайтън код в SQL, ползваме го когато правим create, alter и delete на таблица
    - използвайки RunPython в 95% от случаите няма да ни се наложи да ползавме Scheme Editor, освен, ако не правим някаква временна таблица индекси или промяна             схемата на таблицата
  - Стъпки:
    - Създаваме празен файл за миграция: makemigrations --empty main_app - прави празна миграция в зададен от нас app
    - Дефиниране на операции - Използваме RunPython за да изпълним data migrations
    - Прилагане на промените - migrate

Пример с временна таблица:

Да приемем, че имате модел с име „Person“ във вашето Django приложение и искате да създадете временна таблица, за да съхранявате някои изчислени данни въз основа на съществуващите данни в таблицата „Person“. В този случай можете да използвате мигриране на данни, за да извършите тази операция:

- **Create the Data Migration**:
  - Run the following command to create a data migration:
  ```
  python manage.py makemigrations your_app_name --empty
  ```
- **Edit the Data Migration:**
  - Open the generated data migration file and modify it to use RunPython with a custom Python function that utilizes the SchemaEditor to create a temporary table.       Here's an example:
  ```
  from django.db import migrations, models

  def create_temporary_table(apps, schema_editor):
      # Get the model class
      Person = apps.get_model('your_app_name', 'Person')
  
      # Access the SchemaEditor to create a temporary table
      schema_editor.execute(
          "CREATE TEMPORARY TABLE temp_person_data AS SELECT id, first_name, last_name FROM your_app_name_person"
      )
  
  def reverse_create_temporary_table(apps, schema_editor):
      schema_editor.execute("DROP TABLE temp_person_data")
  
  class Migration(migrations.Migration):
  
      dependencies = [
          ('your_app_name', 'previous_migration'),
    ]

    operations = [
        migrations.RunPython(create_temporary_table, reverse_create_temporary_table),
    ]
  ```

- Django admin
  - createsuperuser
  - Register model, example:

  ```
  @admin.register(OurModelName)
  class OurModelNameAdmin(admin.ModelAdmin):
	  pass
  ```
- Admin site customizations
  - str метод в модела, за да го визуализираме в админ панела по-достъпно
  - list_display - Показваме различни полета още в админа Пример:
  
  ```
  class EmployeeAdmin(admin.ModelAdmin):
	  list_display = ['job_title', 'first_name', 'email_address']
  ```
  - List filter - добавя страничен панел с готови филтри Пример:
  
  ```
   class EmployeeAdmin(admin.ModelAdmin):
 	    list_filter = ['job_level']
   ```
  - Searched fields - казваме, в кои полета разрешаваме да се търси, по дефолт са всички Пример:
  
  ```
  class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['email_address']
  ```
  - Layout changes - избираме, кои полета как и дали да се появяват при добавяне или промяна на запис Пример:

  ```
  class EmployeeAdmin(admin.ModelAdmin):
    fields = [('first_name', 'last_name'), 'email_address']
  ```
  - list_per_page
  - fieldsets - променяме визуално показването на полетата Пример:

  ```
    fieldsets = (
       ('Personal info',
        {'fields': (...)}),
       ('Advanced options',
        {'classes': ('collapse',),
       'fields': (...),}),
      )
  ```

## 04.Data Operations in Django with Queries

- CRUD overview
  - Използваме го при:
    - Web Development
    - Database Management
  - Дава ни един консистентен начин, за това ние да създаваме фунцкионалност за CRUD
  - Можем да го правим през ORM-a на Джанго

- Мениджър в Django:
 - Атрибут на ниво клас на модел за взаимодействия с база данни.
 - Отговорен за CRUD
 - Custom Manager: Подклас models.Model.
   - Защо персонализирани мениджъри:
     - Капсулиране на общи или сложни заявки
     - Подобрена четимост на кода.
     - Избягваме повторенията и подобряваме повторната употреба.
     - Промяна наборите от заявки според нуждите.
- Django Queryset
 - QuerySet - клас в пайтън, който използваме, за да пазим данните от дадена заявка.
 - Данните не се взимат, докато не бъдат потърсени от нас.
 - cars = Cars.objects.all() # <QuerySet []>
 - print(cars) # <QuerySet [Car object(1)]>
 - QuerySet Features:
   - Lazy Evaluation - примера с колите, заявката не се вика, докато данните не потрябват
   - Retrieving objects - можем да вземаме всички обекти или по даден критерии
   - Chaining filters - MyModel.objects.filter(category='electronics').filter(price__lt=1000)
   - query related objects - позволява ни да търсим в таблици, с които имаме релации, през модела:
     #Query related objects using double underscores related_objects = Order.objects.filter(customer__age__gte=18) 
   - Ordering - ordered_objects = Product.objects.order_by('-price')
   - Pagination
    ```
    from django.core.paginator import Paginator

    # Paginate queryset with 10 objects per page
    paginator = Paginator(queryset, per_page=10)
    page_number = 2
    print([x for x in paginator.get_page(2)])
   ```
- Object Manager - default Objects
- Methods:
 - all()
 - first()
 - get(**kwargs)
 - create(**kwargs)
 - filter(**kwargs)
 - order_by(*fields)
 - delete()

- Django Shell and SQL Logging
 - Django Shell
  - Дава ни достъп до целия проект
  - python manage.py shell
- SQL logging
 - Enable SQL logging
 ```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Other levels CRITICAL, ERROR, WARNING, INFO, DEBUG
    },
    'loggers': {
        'django.db.backends': {  # responsible for the sql logs
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```
---
## 05.Working with queries

- Useful Methods
  - filter() - връща subset от обекти; приема kwargs; връща queryset;
  - exclude() - връща subset от обекти; приема kwargs; връща queryset;
  - order_by() - връща сортираните обекти; - за desc;
  - count() - като len, но по-бързо; count връща само бройката без да му трябват реалните обекти;
  - get() - взима един обект по даден критерии;
- Chaning methods
  - всеки метод работи с върнатия от предишния резултат
- Lookup keys
  - Използват се във filter, exclude, get;
  - __exact __iexact - матчва точно;
  - __contains __icontains - проверява дали съдържа;
  - __startswith __endswith
  - __gt __gte
  - __lt __lte
  - __range=(2, 5) - both inclusive
- Bulk methods
  - използват се за да извършим операции върху много обекти едновременно
  - bulk_create - създава множество обекти навъеднъж;
  - filter().update()
  - filter().delete()

---
## 06.Django Relations

Django Models Relations

- Database Normalization
 - Efficient Database Organization
  - Data normalization - разбива големи таблици на по-малки такива, правейки данните по-организирани.
  - Пример: Все едно имаме онлайн магазин и вместо да пазим име, адрес и поръчка в една таблица, можем да разбием на 3 таблици и така да не повтаряме записи.

- Guidelines and Rules
 - First Normal Form
  - First Normal Form (1NF): елеминираме поврарящите се записи, всяка таблица пази уникални стойности
  - Second Normal Form (2NF): извършваме първото като го правим зависимо на PK
   - Пример: Онлайн магазин с данни и покупки Customers и Orders са свързани с PK, вместо всичко да е в една таблица

- Third Normal Form (3NF): - премахване на преходни зависимости - Таблица служители пази id, служител, град, адрес => разделяме ги на 3 таблици и ги навързваме, без да е задължително по PK, може и по city_id вече employee е независимо.
 - Boyce-Codd Normal Form (BCNF):
  - По-строга версия на 3NF
  - Тук правим да се навързват по PK

- Fourth Normal Form (4NF):
 - Ако данни от една таблица се използват в други две то това не е добре.
 - Пример: Имаме Курс X и Курс Y, на X Му трябват книгите A и B, на Y, A и C, това, което правим е да направим таблица с книгите А и таблица с Книгите Б.

- Fifth Normal Form (5NF) - Project-Join Normal Form or PJ/NF:
 - Кратко казано да не ни се налага да минаваме през таблици с данни, които не ни трябват, за да достигнем до таблица с данни, която ни трябва

- Database Schema Design
 - Създаването на различни ключове и връзки между таблиците

- Minimizing Data Redundancy
 - Чрез разбиването на таблици бихме имали отново намалено повтаряне на информация
 - Имаме книга и копия, копията са в отделна таблица, и са линкнати към оригинала

- Ensuring Data Integrity & Eliminating Data Anomalies
 - Това ни помага да update-ваме и изтриваме данните навсякъде еднакво
 - Oтново благодарение на някакви constraints можем да променим една стойност в една таблица и тя да се отрази във всички

- Efficiency and Maintainability
 - Благодарение на по-малките таблици, ги query–ваме и update-ваме по-бързо

- Релации в Django Модели
 - Получават се използвайки ForeignKey полета
 - related_name - можем да направим обартна връзка
  - По дефолт тя е името + _set
- Пример:
  ```
  class Author(models.Model):
    name = models.CharField(max_length=100)

  class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
  ```

- Access all posts written by an author
  ```
  author = Author.objects.get(id=1)
  author_posts = author.post_set.all()
  ```

- Types of relationships
 - Many-To-One (One-To-Many)
 - Many-To-Many
  - Няма значение, в кой модел се слага
  - Django автоматично създава join таблица или още наричана junction
  - Но, ако искаме и ние можем да си създадем:
```
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, through='AuthorBook')

class AuthorBook(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publication_date = models.DateField()
```
 - OneToOne, предимно се слага на PK
 - Self-referential Foreign Key
  - Пример имаме работници и те могат да са мениджъри на други работници
```
class Employee(models.Model):
    name = models.CharField(max_length=100)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
```
- Lazy Relationships - обекта от релацията се взима, чрез заявка, чак когато бъде повикан
