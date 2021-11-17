## Setting up Django Environment
![Minion](https://octodex.github.com/images/minion.png)

**Installing Django**
* Create venv
* pip install Django in venv
```python 
python -m django --version
django-admin startproject <app_name>
```
* creates a project folder in venv called ‘mysite’
    * mysite/ - name doesn't matter
        * manage.py - cmd line for Django
        * mysite/ - Python package
        * __init__.py - tells Python this is a python package
        * settings.py - Config for this Django project
        * urls.py - URL declarations, "table of contents". kind of like express 
          routes, 1st arg is path, 2nd arg is what view function to call
        * asgi.py - connection to webserver (ASGI = async server python)
        * wsgi.py - connection to webserver

**Starting Server**
* python manage.py runserver
* use `python manage.py runserver 8080` for port 8080 or whatever you want
    
**Create new App**
* `python manage.py startapp polls` - creates directories for polls app: 
* polls/
    * __init__.py
    * admin.py
    * apps.py
    * migrations/
    * --> __init__.py
    * --> models.py
    * --> tests.py
    * --> views.py
* create view function in views.py
* create urls.py in polls/ route group for *polls*
    ```python
    from django.urls import path
    from . import views

    urlpatters = [
        path('', views.index, name='index') # name is user friendly name
    ]
    ```
* update admin (mysite) urls to include polls url as a route group for entire *Project*
    ```python
    path('polls/', include('polls.urls'))
    ```

**path() argument**
1) route - req = string that contains URL pattern. Starts from top and searches until matched.
2) view - req = view function, needs an HttpRequest object as the first argument
3) kwargs - opt = keyword arguments in a dictionary. learn more later
4) name - opt = user-friendly name to reference across project

***
## Databases

**Connecting to DB**
* `pip install psycopg2`
* go to settings.py to configure DATABASE variable
* create db in psql
* `python manage.py migrate` - Synchronizes the database state with the current set of models and migrations.

**settings.py:**
* connect to database - DATABASES global variable.
* set time_zone - TIME_ZONE.
* look at installed apps - INSTALLED_APPS.
    admin, auth, contenttypes, sessions, messages, staticfiles
    can comment out before doing migrate

**Creating Models & Using Databases**

* Question / Choice -> instance of django.db.models.Model
* fields are: question_text -> instance of Field class
* fields name = column name
* Some field classes have required args, varies from field to field

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published') #'date published' = specified name, otherwise default is machine-readable name


class Choice(models.Model):
    #1 question to many choices declaration
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0) 
```

**Migrations**
1) Create classes in models.py
2) Make migrations for those changes to models: 
    a) add app to mysite config - `INSTALLED_APPS = ['polls.apps.PollsConfig',`
    b) make snapshot of model changes 
      `python manage.py makemigrations polls` 
     This creates a python file in migrations to show details about the db setup.
     `python manage.py sqlmigrate polls 0001` to see details.
3) Apply changes by: 
     `python manage.py migrate`
     (upon initialization, it creates model tables in database)

*Creating Data*
```python
from polls.models import Choice, Question
from django.utils import timezone #needed for example

q = Question(question_text="What's new?", pub_date=timezone.now())
q.save() #db.session.commit

q.id #returns id of 1.

#update value - 
q.question_text = 'what is up?'
q.save() #db.session.commit
```
**Add string method user friendly name - within Model Class**
```python
def __str__(self):
    return self.choice_text
```

*Looking at Data*
* `Question.objects.all()`
* `Question.objects.filter(id=1)`
* `Question.objects.filter(question_text__startswith='What')`
* `Question.objects.get(pub_date__year=current_year)`
* `Question.objects.get(pk=1)`
* `Question.objects.get(id=2)`
    * error looks like:
        ```
        Traceback (most recent call last):
        ...
        DoesNotExist: Question matching query does not exist.
        ```

*Adding Relational Data*
* store instance: `q = Question.objects.get(pk=1)`
* `q.choice_set.all()` - displays current relational data
* `q.<FK_Table>_set.create(__='', __=)`
* `q.choice_set.create(choice_text='Not much', votes=0)`
* `q.choice_set.create(choice_text='The sky', votes=0)`
* `c = q.choice_set.create(choice_text='Just hacking again', votes=0)`
    * FK class will have access to relationships
    c.question -> <Q: What's up?>
* delete: 
    c = q.choice_set.filter(choice_text__startswith='Just hacking')
    c.delete()

***
## Routing

**URLConf**
* One urlconf file for whole project
* Individual urlconf for each app
    * include namespace so each app's html files are unique
    * `app_name = 'polls'` --> add to polls/urls.py
    * then in templates, reference url 'polls:detail' instead of 'detail'

**Django Views**

* Each view is a python function / class method
* Needs to do either 1) Return HttpResponse object
                     2) Raise exception like Http404
* request.POST - **string values** of a dictionary-like obj for submitted data by key name. 
               - acces via request.POST['<key>']
* request.GET - **string values** of a dictionary-like obj for supplied get data by key name. 
               - acces via request.GET['<key>']
* HttpResponseRedirect(URL)

**Templates**
* make template folder for each app
* put html templates within: <app_name>/templates/<app_name>/index.html
* configs are in TEMPLATES
* import django.shortcuts import render
    `render(request, 'polls/index.html', context)`
    1) request - standard
    2) template name
    3) context - dictionary of var names/values you use in the template
                e.g.     `context = {'latest_question_list': latest_question_list}`
                in template, can use like `{% if latest_question_list %}`
* uses dot-lookup syntax to access variable attributes
* in templates for loop probably don't need to use () to make method-calls. (similar to callbacks)
* accessing url info: 
    w/out namespace: `<a href="{% url 'detail' question.id %}">{{ question.question_text }}</a>`
    w/ namespace: `<a href="{% url 'polls: detail' question.id %}">{{ question.question_text }}</a>` 
* Can use {{ forloop.counter }} within templates - this keeps track of how many times the for tag has gone through its loop
* `reverse('polls:results', args=(question.id,))` -> instead of hardcoding url, django will take in the args and create the url according to the url patterns. This way if you update the urlpattern, you don't have to update it in the view function.

*raising errors*
```python
from django.http import Http404
#SHORTCUT
question = get_object_or_404(Question, pk=question_id)
OR get_list_or_404() #List of objects
#MANUAL WAY
except Question.DoesNotExist:
    raise Http404("Question does not exist")
```

**Django Generic Views**

* needs to know what model - `model = Question`
* template_name is default to `<app name>/<model name>_detail.html`
  otherwise, specify with template_name = 'polls/detail.html'
* provide context if necessary:
    * if it is a Django model (ie Question), it will auto-find generate question_list
    * if not, be specific and specify `context_object_name = 'latest_question_list'`

```python
from django.views import generic
from .models import Choice, Question
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
```

* ListView - display a list of objects
    - uses get_queryset() to determine the list. By default it will give you everything in the Model
    - to customize, define a function `def get_queryset(self): ... `
    - get_context_data() - by default gets everything provided in the context data
        - to customize, you can add things to the dictionary.

* DetailView - display a detail page for a kind of object
    * expects primary key captured from url to be pk

## Django Admin Generics
**Django Admin**
* Django auto creates an admin site with pre-defined groups, users that are managed in the database*
* 1st time accessing it, create a user in terminal:
    `python manage.py createsuperuser`
* run server and go to /admin

**Admin Forms**
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page

* register model class (i.e. Question)
* can add options to customize look
```python
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    #OR
    fields = ['pub_date', 'question_text']
admin.site.register(Question, QuestionAdmin)
```

fieldsets: [form_header, {'fields': ['field_names', ...]}]
or simple verion with no headers
fields = ['field_names', ...]

**Adding relational data to admin form**

*basic way:*
* register model in admin
* foreignkeys will be represented in a select box by default (1-M)

*advanced way:*
* add inlines = [Inline_Class] to primary table (1)
* make Inline_Class for the many table
    * model = Model_Name
    * extra = # of extra boxes to display
    * can be instance of admin.StackedInline or admin.TabularInline (probs has more options too. purely visual difference)
* register primary class normally.

*modifying change list*

* by default django displays the str() of each obj
* add list_display = tuple of field names to display (as columns) to display more details
* to give more user-friendly column names, go to the MODEL itself and add a @admin.display() decorator on the class.

*adding search functionality*
* add `search_fields = ['question_text']` to ModelAdmin admin.py 

```python
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
django.contrib.admin.AdminSite.site_header #use to change site header from default django one
```
*modifying templates*

## Testing

*unit tests*
* within app, put tests in tests.py 
* run tests with `manage.py test polls` --> within polls app, run all tests
* finds subclass of django.test.TestCase class
    * creates test db
    * finds test methods STARTS WITH 'test'

**View tests**

*in shell*
`from django.test.utils import setup_test_environment`
`setup_test_environment()`
! does not setup test database !

```python
from django.test import Client


client = Client() #instantiates client instance to get access to client
response = client.get(reverse('polls:index'))
response.status_code
response.content
response.context['latest_question_list']
```
***
## Python Packaging

**Requirements for making a custom package**
- pip install setuptools
- parent directory of app itself outside of the project (start name w/ django recommended)
- README.rst
    * name of app
    * quick start
- LICENSE file - django default uses BSD-3-CLAUSE
- setup.cfg [see footnote setup.cfg]
- setup.py [see footnote setup.py]
- docs directory
- MANIFEST.in - add other files besides Python modules & packages
    - need to include templates, readme, license, docs, etc.
    - individual files: `include <filename>`
    - directories: `recursive-include <dir/subdir>` ex. polls/static
- build package run within django-polls:
```python
python setup.py sdist
```

**Install package into Django Project**

* `python -m pip install django-polls/dist/django-app-0.1.tar.gz`
* add `--user` if not in venv

***
**Footnotes**

**1) setup.cfg:** includes config details
```python
[metadata]
name = django-polls
version = 0.1
description = A Django app to conduct Web-based polls.
long_description = file: README.rst
url = https://www.example.com/
author = Your Name
author_email = yourname@example.com
license = BSD-3-Clause  # Example license
classifiers =
    Environment :: Web Environment
    Framework :: Django
    Framework :: Django :: X.Y  # Replace "X.Y" as appropriate
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Operating System :: OS Independent
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8
    Topic :: Internet :: WWW/HTTP
    Topic :: Internet :: WWW/HTTP :: Dynamic Content

[options]
include_package_data = true
packages = find:
python_requires = >=3.6
install_requires =
    Django >= X.Y  # Replace "X.Y" as appropriate
```

**2) setup.py:** runs setup command.
```python
from setuptools import setup
setup()
```

**High Level Notes**
- Web pages and other content are delivered by views
- Views are Python functions
- Django will choose a view by examining the URL that’s requested
- URLconf maps URL patterns to views
    - 1st goes to root_urlconf, finds var urlpattersn, traverses in order.
    - matches 'polls/', strips off matching text and goes to app urlconf to process rest of text
    - matches <int:question_id>/ and then calls the view function detail.

**Random Notes**

* lambda = anonymous functions: lambda *arguments : expression*
    * `lambda a : a * n`
* DIRS is a list of filesystem directories to check when loading Django templates; it’s a search path.
* if APP_DIRS is set to True, django will always search for the default admin templates after searching within each app's template folders.
* django templates are in the venv/lib/python3.9/site-packages/django ... 
* where is django? 
```
python -c "import django; print(django.__path__"
````

* `mv folder_from/ company_projects/folder_to`

```
git pull

# this is needed only if the database schema has changed --
# but there's no downside to always doing this
python manage.py migrate

# this is needed only if the CSS/JS has changed --
# but there's no downside to always doing this
python manage.py collectstatic --no-input
```