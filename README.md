# Work-at-Olist test

## Contents

- [Description](#description)
- [Installation](#installation)
- [Deployment](#deployment)
- [Import](#import)
- [API](#api)
- [Test Specification](#test-specification)

## Description

This code refers to my implementation of the 
[challenge](https://github.com/olist/work-at-olist) specified by 
[Olist](https:github.com/olist/) for the Python Developer position. 
It is a Django project designed to import a CSV file and retrieve stored data 
via REST API. 

I developed and tested the code under different environments, but 
 mainly at my Arch Linux machine and a Debian virtual machine, always using 
 virtualenv. As for code development and versioning, I use
 [git flow](https://danielkummer.github.io/git-flow-cheatsheet/) practices
  and I always bear in mind the KISS philosophy (Keep it Simple, Stupid).
 
There are three additional python packages inside the project:
1. api/ - Contains the code related to the Django REST Framework.
    - The endpoints are described at the *API* section of this README file. 
    For the purpose of this test, which required very basic data retrieval,
    I used generic API Views from the REST framework library. I did add a 
    pagination integration, which returns a JSON object instead of a pure array.
    
2. integration/ - Contains the definitions of channels and categories and the 
command for importing categories.
    - The test specification suggested optimizing for tree data reading. I did 
    read about some packages that help with this, such as MPTT, but I figured I 
    could optimize it on my own. Therefore, I came up with a reference creation 
    algorithm that guarantees all objects have unique references and at the same
     time keeps track of the tree path up to the current node. I then defined 
     database indexing on the reference fields to speed up the queries. This 
     permits quickly building a query that finds the desired object in the 
     minimum amount of time (considering it exists).
     - The command for importing categories will print a feedback of its 
     behavior if `settings.DEBUG` is enabled. How to use it is described in the 
     *Importation* section of this README file.
3. settings/ - Contains three settings files: 
    base.py, local.py and production.py
    - The production settings file retrieves database connection information 
    from environment variables. 


## Installation

For the purpose of installing this project locally, you will need the following 
packages:

- Python3.6
- Pip
- PostgreSQL

Clone this repository onto your desired machine and install the project 
requirements

```
$ git clone https://github.com/thiagorcdl/work-at-olist
$ cd work-at-olist/
$ pip install -r requirements-local.txt
```

Now, make sure your database schema is up do date, by running the migration 
scripts:
```
$ cd work-at-olist/
$ python manage.py migrate
```

## Deployment
This project includes a *Procfile* for [Heroku](http://heroku.com) integration.
The easiest way for deploying a copy of this app is using Heroku's web 
interface and using GitHub integration.
- Fork this repository using your GitHub account.
- Go to Heroku dashboard and create a new app on the upper-right corner menu.
- Configure the environment variables under the *Settings* tab:
    - DJANGO_SETTINGS_MODULE=settings.production
    - DISABLE_COLLECTSTATIC=1
- Set up the project integration under the *Deploy* tab. 
- When you are done, click on the *Deploy Branch* button.

Don't forget to run the migration scripts. Every command that follows might also
 be executed at your deployment environment using either the Heroku-CLI or the 
 web interface for sending commands.

```
$ heroku run python work-at-olist/manage.py migrate
```

## Usage

### Import

Once you have all the required packages properly installed and 
[Postgres server running](http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html),
 you can run the `importcategories` command.
 This command expects the following two parameters:
 - A channel name
 - A CSV file containing a column named *"Category"*
 
```
$ python manage.py importcategories <channel_name> <path/to/file.csv>
```

 For example, if you have a file in your home folder called 
 "categories_list.csv" which lists categories related to channel *Marketplace*, 
 you may run the following:
 
 ```
 $ python manage.py importcategories Marketplace ~/categories_list.csv
 ```


### API

There are four endpoints for retrieving data. The test specified three 
endpoints, however, due to the lack of clarification on one of them, I decided 
to cover two possible interpretations.

#### Channel List
Returns a list that contains all existing channels.

Method: `GET`

URL: `/api/channels/`

URL Parameters:
- Required: *none*
- Optional:
    - offset \<int>: Amount of objects to skip.
    - limit \<int>: Maximum amount of objects to retrieve.

Response:
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "MyChannel",
            "reference": "mychannel"
        },
        {
            "name": "MyChannel2",
            "reference": "mychannel2"
        }
    ]
}
```

#### Channel's Categories List
Returns every Category for a given Channel.

Method: `GET`

URL: `/api/channels/categories/{{channel_reference}}/`

URL Parameters:
- Required:
    - channel_reference \<str>: The reference of an existing Channel object.
- Optional:
    - offset \<int>: Amount of objects to skip.
    - limit \<int>: Maximum amount of objects to retrieve.

Response (with limit=2):
```
{
    "count": 23,
    "next": "<base_url>/api/channels/categories/mychannel/?limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "name": "Books",
            "reference": "mychannel_books"
        },
        {
            "name": "Foreign Literature",
            "reference": "mychannel_books_foreign-literature"
        }
    ]
}
```


#### Category Detail
Returns a single Category with its parent and children categories 
(directly related)

Method: `GET`

URL: `/api/categories/{{category_reference}}/`

URL Parameters:
- Required:
    - category_reference \<str>: The reference of an existing Category object.
- Optional: *none*

Response:
```
{
    "name": "National Literature",
    "reference": "mychannel_books_national-literature",
    "parent": {
        "name": "Books",
        "reference": "mychannel_books"
    },
    "children": [
        {
            "name": "Science Fiction",
            "reference": "mychannel_books_national-literature_science-fiction"
        },
        {
            "name": "Fiction Fantastic",
            "reference": "mychannel_books_national-literature_fiction-fantastic"
        }
    ]
}
```


#### Related Categories List
Returns a list with the requested category, 
all of its ancestors and descendants.

Method: `GET`

URL: `/api/categories/related/{{category_reference}}/`

URL Parameters:
- Required:
    - category_reference \<str>: The reference of an existing Category object.
- Optional:
    - offset \<int>: Amount of objects to skip.
    - limit \<int>: Maximum amount of objects to retrieve.

Response:
```
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Books",
            "reference": "mychannel_books"
        },
        {
            "name": "National Literature",
            "reference": "mychannel_books_national-literature"
        },
        {
            "name": "Fiction Fantastic",
            "reference": "mychannel_books_national-literature_fiction-fantastic"
        }
    ]
}
```

## Test Specification

The following is the test's original README.md content.

### Work at Olist

Olist is a company that offers an integration platform for sellers and
marketplaces allowing the former to sell their products across multiple channels.

The Olist development team consists of developers who love what they do. Our
agile development processes and our search for the best development practices
provide the perfect environment for professionals who like to create quality
software.

We are always looking for good programmers who love to improve their work and
we give preference to small teams with qualified professionals to large teams
with average professionals.

This repository contains a small test used to evaluate if the candidate has the
basic skills to work with us.

You should implement a Django application that provides an API for handling a
tree of products' categories.


#### How to participate

1. Make a fork of this repository on Github. If you can't create a public
   fork of this project at Github, make a private repository in 
   [bitbucket.org](https://bitbucket.org) (for free) and add read permission
   for user [@osantana](https://bitbucket.org/osantana) on project.
2. Follow the instructions of `README.md`.
3. Deploy you project on [Heroku](https://heroku.com).
4. Apply for the position at our [career page](http://bit.ly/olist-webdev) and send:
  - Link to the fork on GitHub (or [bitbucket.org](https://bitbucket.org)) .
  - Link to the project in [Heroku](https://heroku.com).
  - Brief description of the work environment used to develop this project
    (Computer/operating system, text editor/IDE, libraries, etc.).


#### Specification

As we already said, Olist is a company that provides a platform to integrate
sellers and channels (eg. marketplaces).

One of our services allows sellers to publish their products in channels. All
published products need to be categorized in one of the channels' categories.

All channels group the published products in categories that are arranged as a
tree of *varying depths* (from 1 to infinite levels of hierarchy). The list below exemplifies the categories tree:

- Books
  - National Literature
    - Science fiction
    - Fantastic Fiction
  - Foreign literature
  - Computers
    - Applications
    - Database
    - Programming
- Games
  - XBOX 360
    - Console
    - Games
    - Accessories
  - XBOX One
    - Console
    - Games
    - Accessories
  - Playstation 4
- Computing
  - Notebooks
  - Tablets
  - Desktop
- :

Each channel sends us a CSV file where one of the columns (`Category`) contains the full category's path:

```
Category
Books
Books / National Literature
Books / National Literature / Science Fiction
Books / National Literature / Fiction Fantastic
Books / Foreign Literature
Books / Computers
Books / Computers / Applications
Books / Computers / Database
Books / Computers / Programming
Games
Games / XBOX 360
Games / XBOX 360 / Console
Games / XBOX 360 / Games
Games / XBOX 360 / Accessories
Games / XBOX One
Games / XBOX One / Console
Games / XBOX One / Games
Games / XBOX One / Accessories
Games / Playstation 4
Computers
Computers / Notebooks
Computers / Tablets
Computers / Desktop
:
```


#### Project Requirements

The project must implement the following features:

- Python >= 3.5 and Django >= 1.10.
- Use PEP-8 for code style.
- The data should be stored in a relational database.
- A *Django Management Command* to import the channels' categories from a CSV.
  - Import command should operate in "full update" mode, ie it must overwrite
    all categories of a channel with the categories in CSV.
  - The command should receive 2 arguments: channel name (create the channel if
    it doesn't exists in database) and the name of `.csv` file:

```
$ python manage.py importcategories walmart categories.csv
```

- Each channel has its own set of categories.
- Each channel must have a unique identifier and a field with the channel's
  name.
- Each category must have a unique identifier and a field with the category's
  name.
- Creating a HTTP REST API that provides the following functionalities:
  - List existing channels.
  - List all categories and subcategories of a channel.
  - Return a single category with their parent categories and subcategories.

> Tip #1:
> Optimize for category tree read performance!

- English documentation of API.
- Variables, code and strings must be all in English.

> Tip #2:
> Django project boilerplate in this repository has several points for
> improvement. Find them and implement these improvements.


#### Recommendations

- Write tests.
- Avoid exposing database implementation details in the API (eg. do not expose model ID at URLs)
- Practice the [12 Factor-App](http://12factor.net) concepts.
- Make small and atomic commits, with clear messages (written in English).
- Use good programming practices.
