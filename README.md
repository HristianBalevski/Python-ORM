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

---
## 07.Models Inheritance and Customization

- Типове наследяване
  - Multi-table
    - Разширяваме модел с полетата от друг модел, като не копираме самите полета, а използваме създадения от django pointer, който прави One-To-One Relationship
    - Пример:
```
class Person(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    def is_student(self):
        """Check if this person is also a student."""
        return hasattr(self, 'student')

class Student(Person):
    student_id = models.CharField(max_length=15)
    major = models.CharField(max_length=50)
```
 - Abstract Base Classes
   - При това наследяване не се създават две нови таблици, а само една и тя е на наследяващия клас(Child), като абстрактния клас(Parent) е само шаблон
   - Постигаме го чрез промяна на Meta класа:
```
class AbstractBaseModel(models.Model):
    common_field1 = models.CharField(max_length=100)
    common_field2 = models.DateField()

    def common_method(self):
        return "This is a common method"

    class Meta:
        abstract = True
```

- Proxy Models
  - Използваме ги, за да добавим функционалност към модел, който не можем да достъпим
  - Можем да добавяме методи, но не и нови полета
  - Пример:
```
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField()

class RecentArticle(Article):
    class Meta:
        proxy = True

    def is_new(self):
        return self.published_date >= date.today() - timedelta(days=7)
    
    @classmethod
    def get_recent_articles(cls):
        return cls.objects.filter(published_date__gte=date.today() - timedelta(days=7))
```

- Основни Built-In Методи
  - save() - използва се за запазване на записи
```
    def save(self, *args, **kwargs):
        # Check the price and set the is_discounted field
        if self.price < 5:
            self.is_discounted = True
        else:
            self.is_discounted = False

        # Call the "real" save() method
        super().save(*args, **kwargs)
```

  - clean() - използва се, когато искаме да валидираме логически няколко полета, например имаме тениска в 3 цвята, но ако е избран XXL цветовете са само 2.

- Custom Model Properties
  - Както и в ООП, можем чрез @property декоратора да правим нови атрибути, които в случая не се запазват в базата
  - Използваме ги за динамични изчисления на стойностти

- Custom Model Fields
  - Ползваме ги когато, Django няма field, който ни върши работа
  - Имаме методи като:
    - from_db_value - извиква се, когато искаме да взмем стойността от базата в пайтън
    - to_python
       - Използва се, когато искаме да преобразуваме стойности от базата данни или външен формат към Python обект, който може да бъде обработван в нашия код.
         - Преобразуване на стойности от базата данни: Когато извличаме стойности от базата данни и искаме да ги преобразуваме в Python обекти.
         - Валидация на стойности: Можем да използваме to_python за валидация на стойности преди да бъдат записани или използвани в моделите.
         - Преобразуване на външни данни: Ако имаме например данни от формуляри, можем да използваме to_python, за да преобразуваме тези данни в Python обекти.
    - get_prep_value - обратното на from_db_value, от Python към базата, предимно ползваме за сериализации
    - pre_save - използва се за last minute changes, точно преди да запазим резултата в базата
    - clean() - Методът clean() се използва за валидация и обработка на данни, преди те да бъдат записани в базата данни или преди да бъдат използвани във формата.
   
```
class RGBColorField(models.TextField):
    # Convert the database format "R,G,B" to a Python tuple (R, G, B)
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return tuple(map(int, value.split(',')))

    # Convert any Python value to our desired format (tuple)
    def to_python(self, value):
        if isinstance(value, tuple) and len(value) == 3:
            return value
        if isinstance(value, str):
            return tuple(map(int, value.split(',')))
        raise ValidationError("Invalid RGB color format.")

    # Prepare the tuple format for database insertion
    def get_prep_value(self, value):
        # Convert tuple (R, G, B) to "R,G,B" for database storage
        return ','.join(map(str, value))
```
---
## 08.Advanced Django Models Techniques

- Validation in Models
  - Built-in Validators
    - MaxValueValidator, MinValueValidator - приема два аргумета (limit, message)
    - MaxLengthValidator, MinLengthValidator - приема два аргумета (limit, message)
    - RegexValidator - приема два аргумета (regex, message)
```
class SampleModel(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(5)]  # Name should have a minimum length of 5 characters
    )

    age = models.IntegerField(
        validators=[MaxValueValidator(120)]  # Assuming age shouldn't exceed 120 years
    )

    phone = models.CharField(
        max_length=15,
        validators=[
	    RegexValidator(
	        regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
	)]  # A simple regex for validating phone numbers
    )
```
- Custom Validators - функции, които често пишем в отделен файл. При грешка raise-ваме ValidationError

- Meta Options and Meta Inheritance
   - В мета класа можем да променяме:
     - Името на таблицата
     - Подреждането на данните
     - Можем да задаваме constraints
     - Можем да задаваме типа на класа(proxy, abstract)
```
class SampleModel(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField()

    class Meta:
        # Database table name
        db_table = 'custom_sample_model_table'

        # Default ordering (ascending by name)
        ordering = ['name'] - Случва се на SELECT, не на INSERT

        # Unique constraint (unique combination of name and email)
        unique_together = ['name', 'email']
```
- Meта наследяване:
  - Ако наследим абстрактен клас и не презапишем мета класа, то наследяваме мета класа на абстрактния клас
```
class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        abstract = True
        ordering = ['name']

class ChildModel(BaseModel):
    description = models.TextField()
    # ChildModel inherits the Meta options
```
- Indexing
  - Индексирането ни помага, подреждайки елементите в определен ред или създавайки друга структура, чрез, която да търсим по-бързо.
  - Бързо взимаме записи, но ги запазваме по-бавно
  - В Django можем да сложим индекс на поле, като добавим key-word аргумента db_index=True
  - Можем да направим и индекс, чрез мета класа, като можем да правим и композитен индекс
```
class Meta:
indexes=[
models.Index(fields=["title", "author"]),  # прави търсенето по два критерия, по-бързо
models.Index(fields=["publication_date"])
]
```
- Django Model Mixins
  - Както знаем, миксините са класове, които използваме, за да отделим обща функционалност
```
class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
	class Meta:
    	    abstract = True
```
---
## Advanced Queries in Django
1. What is Manager
   - В Django, Manager представлява интерфейс за взаимодействие с данни в моделите. Той дава възможност за извършване на заявки към базата данни и манипулиране на обекти, представляващи записи в тази база. Всеки Django модел по подразбиране има вече създаден мениджър, достъпен чрез objects, но може да бъде създаден и персонализиран Manager за конкретни нужди.

Създаване на персонализиран Manager:
```
from django.db import models

class CustomManager(models.Manager):
    def get_active_users(self):
        return self.filter(is_active=True)

class User(models.Model):
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    objects = CustomManager()  # Свързване на модела с персонализирания мениджър
```
В този пример, създаваме CustomManager, който наследява models.Manager. В него добавяме метод get_active_users, който връща всички активни потребители. После свързваме този мениджър с модела User чрез присвояване на инстанция на CustomManager на атрибута objects на модела.

Кога да създадем персонализиран Manager:

1. **Повторно използване на често използвани заявки:** Ако често използвате определени заявки към базата данни в различни части на вашето приложение, персонализиран мениджър може да улесни повторното използване на тези заявки.

2. **Допълнителна логика за заявките:** Ако искате да добавите допълнителна логика към заявките, например филтриране, подреждане или обработка на резултатите, персонализираният мениджър е подходящо място да добавите тази логика.

3. **Абстракция на базовите заявки:** Мениджърът предоставя абстракция върху базовите заявки, като това улеснява бъдещите промени в заявките, без да се налага промяна в цялото приложение.

4. **Организация на кода:** Персонализираният мениджър помага за по-добра организация на кода, като групира свързаната функционалност на едно място.

5. **Тестване:** Ако искате по-лесно тестване на заявките и логиката, свързана с тях, можете да изолирате функционалността в персонализирания мениджър и да му тествате методите.

Създаването на персонализиран Manager предоставя гъвкавост и четимост на кода, като ефективно управлява заявките и манипулациите с данни във вашия Django проект.

Анотации и агрегации:

- **Анотации (Annotations):**
  - Позволяват добавянето на допълнителни полета към резултатния набор, които са резултат от агрегатни функции или други изчисления.
  ```
  from django.db.models import Count, Sum

  # Анотация с брой постове за всеки потребител
  users_with_post_count = User.objects.annotate(num_posts=Count('post'))

  # Анотация с общ брой постове в системата
  total_posts = Post.objects.aggregate(total_posts=Count('id'))
  ```
- **Агрегации (Aggregations):**
  - Позволяват извличането на агрегирани стойности от резултатния набор.
```
from django.db.models import Avg, Max, Min

# Средна възраст на потребителите
average_age = User.objects.aggregate(avg_age=Avg('age'))

# Максимална и минимална възраст на потребителите
max_age = User.objects.aggregate(max_age=Max('age'))
min_age = User.objects.aggregate(min_age=Min('age'))
```

Използване на F-обекти и Q-обекти:

- **F-обекти:**
  - Позволяват извършването на операции със стойности на полета в базата данни.
```
from django.db.models import F

# Увеличаване на възрастта на всички потребители с 1
User.objects.update(age=F('age') + 1)
```
- **Q-обекти:**
  - Позволяват създаването на сложни условия за заявките.
```
from django.db.models import Q

# Извличане на потребители с възраст под 30 или с потребителско име 'admin'
users = User.objects.filter(Q(age__lt=30) | Q(username='admin'))
```
Използване на Subqueries:

- **Subqueries:**
  - Възможност за използване на подзаявки във нашия SQL, които да бъдат вградени в основната заявка.
```
from django.db.models import OuterRef, Subquery

# Извличане на всички постове, чийто автор е с най-висока възраст
subquery = User.objects.filter(id=OuterRef('author_id')).values('age')[:1]
posts = Post.objects.annotate(author_age=Subquery(subquery)).order_by('-author_age')
```
Тези заявки в Django ни позволяват да извличаме по-сложна информация от базата данни, като в същото време поддържат четимост и ефективност на нашия код. Използването на агрегации, анотации и разширени заявки дава възможност за детайлно и точно управление на данните във нашия проект.

- **related_name:**
  - related_name се използва, когато дефинираме обратна връзка (reverse relationship) в модела. Това ни позволява да зададем име на атрибут, който ще бъде използван за достъп до свързаните обекти от другия край на връзката.
```
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```
В този пример, ако искаме да получим всички книги, написани от определен автор, използваме related_name='books'. Сега можем да извършим заявка относно автор и да получим всички свързани книги чрез author.books.all()

- **prefetch_related:**
  - prefetch_related е метод, който предварително извлича данните за свързаните обекти, оптимизирайки броя на заявките към базата данни. Той е полезен, когато имаме много обекти и искаме да избегнем N+1 проблема (множество заявки за свързани обекти), като извличаме всички свързани обекти с една заявка.
```
# Пример с използване на prefetch_related
authors = Author.objects.prefetch_related('books').all()

for author in authors:
    # Няма допълнителни заявки, всички книги са предварително извлечени
    for book in author.books.all():
        print(book.title)
```
Тук, prefetch_related('books') извлича всички свързани книги за всички автори в една заявка, което предотвратява изпълнението на N+1 заявки, когато обхождаме всеки автор.

Като цяло, **related_name** се използва за именуване на обратната връзка и улеснява достъпа до свързаните обекти, докато **prefetch_related** подобрява ефективността, като оптимизира заявките към базата данни, извличайки данните за свързаните обекти предварително. Обичайно се използват заедно, когато искаме да оптимизираме заявките и лесно да обхождаме данните в нашия код.

---
