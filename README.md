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


  
  
