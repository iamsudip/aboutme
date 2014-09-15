=====================================
http://aboutme-iamsudip.rhccloud.com/
=====================================

**I am very bad at naming. If you have suggestion, suggest me. I didn't think of any name for this social appearance site yet.**

Service Description
-------------------

This a social experience site as I said above and more or less like http://about.me/ but not completely copy of it.

TODO
----

For now, First target is make the service alive: like

* Re-build UI, Make use of parallax scrolling in the main page

* not only sign up, give them their own page to create and manipulate their bio

* one click resume making extension

* give user an option to create a blog if she doesn't have one

* and many more, you can always suggest (open an issue here or mail me.)

* Add feature: Github login

* Include Client side validation to make things faster for the user.

Setup
-----

First fork & clone the repo.

Now *before creating and entering into virtualenv* make sure you install the following::

I am using `postgresql-9.1` so you need to install this too.

      $ sudo apt-get install postgresql-9.1

      $ sudo apt-get install postgresql-server-dev-9.1

I am using `bcrypt` to hash the passwords and `bcrypt` depends on `libffi-dev`

	$ sudo apt-get install libffi-dev

I always recommend python-virtualenv for development.

After installing and activating the virtual environment do the follwing

Install the requirements file::

      $ pip install -r requirements.txt

Now, I spent hours fixing many things on my machine, so I want you don't waste the same.

Setup the database server as follows::

      $ sudo -u postgres createuser <your username>

To create the database do this::

      $ createdb aboutmedb 

Now open postgresql as::

      $ psql aboutmedb

      # \password

Enter the password as: passwrd

Repeat the password as: passwrd

'passwrd' is the password without quote

Setup `config.py` according to this username and password as::

	postgresql://username:passwrd@localhost:5432/aboutmedb

I think your local server is ready to roll now.

cd to aboutme/aboutme locate main.py and run::

      $ python main.py

Happy hacking!

