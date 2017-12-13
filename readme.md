# Intro to Web Development for Data Scientists

## Learning Objectives
* Create an app using Flask
* Connect your Flask app to a PostgreSQL database
* Visualize Data using Dimple.js
* View other examples of data science apps

## Framing
One way to show off your data science work or automate your work is to create data analysis applications. Today we will use Flask in order to build a simple data visualization app.

## Setup

First, let's make a directory for the project.
```bash
$ mkdir app
```
Then, lets scaffold our project:
```bash
$ touch app.py
$ mkdir templates
```
Let's also download a text editor and set it up:
Click this link: https://code.visualstudio.com/docs?dv=osx
Then, open the app and press `⇧⌘P`. Then type in `Shell Command: Install 'code' command in PATH`.

Then we should create a `.gitignore` file that will make sure we don't push unneeded files to GitHub. I use [this one](https://github.com/github/gitignore/blob/master/Python.gitignore).

Let's also encapsulate our project in a virtual environment so we keep our versions clean.
```bash
$ virtualenv .env
$ source .env/bin/activate
```
Create a `requirements.txt` file and add the dependencies to it.
```bash
$ touch requirements.txt
$ code requirements.txt
```
Copy and paste this into it:
```
click==6.7
Flask==0.12.2
Flask-SQLAlchemy==2.3.2
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
psycopg2==2.7.3.2
SQLAlchemy==1.1.15
Werkzeug==0.13
WTForms==2.1
```
Then install them:
```bash
$ pip install -r requirements.txt
```

## Building a Basic App
`app.py`
```py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/') # The URL for the page we are creating
def show_candies():
    return render_template('candy_list.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
```

Let's also create the template:
```bash
$ touch templates/candy_list.html
``` 
In there, we will generate some HTML code to scaffold our site.
`HTML:5` and then enter should create a template.
Then, add in the title field and a header.

We can also pass variables from our view function to our template like this:
```py
def show_candies():
    return render_template('candy_list.html', candies="candies")
```
Then we can use the variable in our template like this:
```html
{{ candies }}
```

Let's test it out with these commands:
```bash
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=1
$ python -m flask run
```

## Adding Data
Let's now add dynamic data to our application. I used [this dataset](https://raw.githubusercontent.com/fivethirtyeight/data/master/candy-power-ranking/candy-data.csv) for this application. Let's first set up our model which will hold our data.

```py
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/candy'
db = SQLAlchemy(app)

class Candy(db.Model):
    __tablename__ = "candies"
    id = db.Column(db.Integer, primary_key=True)
    competitorname = db.Column(db.String(120), unique=True)
    chocolate = db.Column(db.Integer())
    fruity = db.Column(db.Integer())
    caramel = db.Column(db.Integer())
    peanutyalmondy = db.Column(db.Integer())
    nougat = db.Column(db.Integer())
    crispedricewafer = db.Column(db.Integer())
    hard = db.Column(db.Integer())
    bar = db.Column(db.Integer())
    pluribus = db.Column(db.Integer())
    sugarpercent = db.Column(db.Float())
    pricepercent = db.Column(db.Float())
    winpercent = db.Column(db.Float())
```

Then let's create the database.
```bash
$ psql
> CREATE DATABASE candy;
> \q
```
Then, let's create the schema:
```bash
$ python
>>> from app import db
>>> db.create_all()
>>> exit()
```
Let's also copy in the seed data
```bash
$ psql candy
candy=# \copy candies(competitorname,chocolate,fruity,caramel,peanutyalmondy,nougat,crispedricewafer,hard,bar,pluribus,sugarpercent,pricepercent,winpercent) FROM '../data.csv' DELIMITER ',' CSV HEADER;
```
Now, let's pass the data to the template.

```py
@app.route('/')
def show_candies():
    candies = Candy.query.all()
    return render_template('candy_list.html', candies=candies)
```
We can then show the candy's results in table form like so:

```html
<table class="table table-hover">
    <thead>
        <th>Candy</th>
        <th>Rating</th>
    </thead>
    <tbody>
        {% for candy in candies %}
        <tr>
            <td>{{ candy.competitorname }}</td>
            <td>{{ candy.winpercent }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

## Visualizing the data
Finally, let's add in a data visualization to show how our candy rankings compare. First, we will add a method to our model:
```py
def display_json():
    return [{
        "name": candy.competitorname,
        "winpercent": candy.winpercent
    } for candy in Candy.query.all()]
```
Let's also pass it to our template
```py
def show_candies():
    candies = Candy.query.all()
    return render_template('candy_list.html', candies=candies, candy_json=Candy.display_json())
```
Finally, let's add Dimple.js to our template to finalize our visualization.
```js
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.12.0/d3.js"></script>
<script src="http://dimplejs.org/dist/dimple.v2.3.0.min.js"></script>
<script>
    let svg = dimple.newSvg("#chart-container", 1000, 500)
    let chart = new dimple.chart(svg, {{ candy_json|tojson|safe }})
    chart.setBounds(60, 30, 800, 300)
    var x = chart.addCategoryAxis("x", "name")
    chart.addMeasureAxis("y", "winpercent")
    chart.addSeries(null, dimple.plot.bar)
    chart.draw()
</script>          
```
## Forms
Finally, let's add a form so that we can add items to our database.
```py
from wtforms import Form, StringField, IntegerField, FloatField

class CandyForm(Form):
    competitorname = StringField('Name')
    chocolate = IntegerField('chocolate')
    fruity = IntegerField('fruity')
    caramel = IntegerField('caramel')
    peanutyalmondy = IntegerField('peanutyalmondy')
    nougat = IntegerField('nougat')
    crispedricewafer = IntegerField('crispedricewafer')
    hard = IntegerField('hard')
    bar = IntegerField('bar')
    pluribus = IntegerField('pluribus')
    sugarpercent = FloatField('sugar percent') 
    pricepercent = FloatField('price percent')
    winpercent = FloatField('win percent')


@app.route('/create', methods=['GET', 'POST'])
def create_candies():
    form = CandyForm(request.form)
    if request.method == 'POST' and form.validate():
        candy = Candy(competitorname=form.competitorname.data, chocolate=form.chocolate.data, fruity=form.fruity.data, caramel=form.caramel.data, 
                      peanutyalmondy=form.peanutyalmondy.data, nougat=form.nougat.data, crispedricewafer=form.crispedricewafer.data,
                      hard=form.hard.data, bar=form.bar.data, pluribus=form.pluribus.data, sugarpercent=form.sugarpercent.data,
                      pricepercent=form.pricepercent.data, winpercent=form.winpercent.data)
        db.session.add(candy)
        db.session.commit()
        return redirect('/')
    return render_template('candy_form.html', form=form)
```

```html
{% macro render_field(field) %}
<dt>{{ field.label }}
<dd>{{ field(**kwargs)|safe }}
{% if field.errors %}
  <ul class=errors>
  {% for error in field.errors %}
    <li>{{ error }}</li>
  {% endfor %}
  </ul>
{% endif %}
</dd>
{% endmacro %}

<form method="post" action="/create">
    <dl>
      {{ render_field(form.competitorname) }}
      {{ render_field(form.chocolate) }}
      {{ render_field(form.fruity) }}
      {{ render_field(form.caramel) }}
      {{ render_field(form.peanutyalmondy) }}
      {{ render_field(form.nougat) }}
      {{ render_field(form.crispedricewafer) }}
      {{ render_field(form.hard) }}
      {{ render_field(form.bar) }}
      {{ render_field(form.pluribus) }}
      {{ render_field(form.sugarpercent) }}
      {{ render_field(form.pricepercent) }}
      {{ render_field(form.winpercent) }}
    </dl>
    <p><input type="submit" value="submit">
</form>
```

## Additional Resources
* [Flask Documentation](http://flask.pocoo.org/docs/0.12/)
* [Flask SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/queries/)
* [Making a Flask app using a PostgreSQL database and deploying to Heroku](http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/)
* [Deploy Machine Learning Models](https://www.analyticsvidhya.com/blog/2017/09/machine-learning-models-as-apis-using-flask/)
* [Data Viz App](https://medium.com/@rchang/learning-how-to-build-a-web-application-c5499bd15c8f)
* [Flowing Data](http://flowingdata.com/)
* [D3](https://d3js.org/)
* [Dimple](http://dimplejs.org/)
* [Deploy Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
