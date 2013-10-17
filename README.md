# andywrote.me

## About

This is the code for my personal website. It is based on Flask and Postgres and is intended to be deployed through Heroku. I have not been wholly disciplined about writing the code in a generic, reusable manner, but it shouldn't be too bad for you to take this code and run your own site should you be interested. 

## Get up and running locally

- Install Python (any reasonably up-to-date version of Python 2; I haven't tested anything with Python 3). Install pip. 

- Install the packages in `requirements.txt` with `pip install -r requirements.txt`. I strongly suggest you create a virtualenv and do it there! 

- Set an environment variable `HEROKU_ENVIRONMENT` to "development". If you use virtualenvwrapper, you can edit your postactivate and postdeactivate hooks (in $VIRTUAL_ENV/bin) to set and unset automatically when you activate/deactivate your virtualenv. Use `export` to set it in postactivate so that it's visible as an environment variable. 

- Install Postgres. If you are using OS X, I recommend Postgres.app, which is painless to install and easy to use. 

- Create a new Postgres user `andywrote` and a new database `andywrote-development` as follows (thanks to this [handy no-frills guide](http://killtheyak.com/use-postgresql-with-django-flask/): 

```
$ createuser -U andywrote <yourusername>
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) n
$ createdb -U <yourusername> -E utf8 -O <yourusername> andywrote-development -T template0
```

- Run a db migration with Alembic: `alembic upgrade head`

- At this point you should be able to run `python serve.py` to get your server up and running locally with Flask's local server, without touching Heroku. 

- Get a Heroku account, create your Heroku app, install the Heroku Toolbelt, login ([detailed instructions](https://devcenter.heroku.com/articles/quickstart)). 

- Run `foreman start` to start the webserver. 

## Deploy to Heroku

Thanks to [this Stack Overflow question](http://stackoverflow.com/questions/13262195/how-should-i-run-alembic-migrations-on-heroku) for help on this. Also, check out [Heroku's docs on using Postgres](https://devcenter.heroku.com/articles/heroku-postgresql) for a more detailed explanation on using Postgres with your Heroku app. 

- Add a Postgres database to your app. As of this writing, Heroku's "Dev"-tier database is free and can be installed with `heroku addons:add heroku-postgresql:dev`, or by navigating the Heroku dashboard on its website. 

- You should now have an environment variable in Heroku of the form `HEROKU_POSTGRESQL_<color>_URL` or something like that. Run `heroku pg:promote HEROKU_POSTGRESQL_<color>_URL` to make this database your primary one. 

- Set Heroku environment variables `FLASK_SECRET_KEY`, `FLASK_SECURITY_PASSWORD_SALT`, and `FLASK_USERNAME` (self-explanatory; they correspond to Flask config variables without `FLASK_`prepended). Use `heroku config:set` to set these. 

- Deploy your app the usual way, `git push heroku master`. 

- Migrate your db with `heroku run alembic upgrade head`. 

## User accounts

You can create a new user locally with `HEROKU_ENVIRONMENT=development python create_user.py`. It will prompt you for inputs. You can do the same on Heroku with `heroku run python create_user.py`. To login to the site, go to /login. 

This website was generally intended as single-user, and so while multiple user accounts is supported, the code is not written with multiple users in mind. There is no obvious link to the login page, there is no way to register a new user through the app, no author pages on the blog, and every user can manage and edit every other user's blog posts. 

The app uses sha512_crypt to store passwords. Make sure that in production you have set `FLASK_SECRET_KEY` and `FLASK_SECURITY_PASSWORD_SALT` to something secure. 

## Credits

- [Rokkitt](http://www.fontsquirrel.com/fonts/list/foundry/vernon-adams) font by Vernon Adams. 
- [Libre Baskerville](http://www.google.com/fonts/specimen/Libre+Baskerville) by [Impallari Type](http://www.impallari.com/) via Google Fonts. 
- [Social network icons](http://sawb.deviantart.com/art/Social-Icons-Pack-123247215) by Sylwia Besz-Miazga. 
- Background created with Doug Zongker's [Celtic Knot Thingy](http://isotropic.org/celticknot/). 

## Licenses

The files `static/font/rokkit-webfont*` are all covered by `static/fonts/rokkitt_license.txt`. The files in `static/images/icons` are covered by [Creative Commons Attribution 3.0](http://creativecommons.org/licenses/by/3.0/us/), with the attribution stipulation: 

> If you use them credit me somewhere on your page (i.e. in a footer) with link to icons http://sawb.deviantart.com/art/Social-Icons-Pack-123247215

Everything else is covered by the MIT license, reproduced below. 

> Copyright (c) 2013 Andrew Lim
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.