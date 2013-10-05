# andywrote.me

## Getting started

Postgres-related instructions assume you're using OS X and Postgres.app, which is how I did it and which I thought was quite painless, although if you're more comfortable with other Postgres distributions they should be fine. 

1. Install Python (any reasonably up-to-date version of Python 2, haven't tested anything with Python 3). Install pip. 

2. Install the packages in `pip.manifest` with `pip install -r pip.manifest`. 

3. Install Postgres.app and launch it. 

4. Create a new Postgres user `andywrote` and a new database `andywrote` as follows (thanks to this [handy no-frills guide](http://killtheyak.com/use-postgresql-with-django-flask/): 

```
$ createuser -U andywrote <yourusername>
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) n
$ createdb -U <yourusername> -E utf8 -O <yourusername> andywrote -T template0

```

5. Run your db migration with Alembic: `alembic upgrade head`

6. Run `python serve.py`. 


## Miscellany

Registration is disabled (this was intended as a single-user website). You can create a user from a Python prompt as follows: 

```
import andywrote
with andywrote.app.app_context():  # must be in application context
    andywrote.create_user(email='your_email', name='your_name', password='your_password')
```

The app uses sha512_crypt to store passwords. 

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