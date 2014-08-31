=====================================
http://aboutme-iamsudip.rhccloud.com/
=====================================

**I am very bad at naming. If you have suggestion, suggest me. I didn't think of any name for this social appearance site yet.**

Service Description
-------------------

This a social experience site as I said above and more or less like http://about.me/ but not completely copy of it.

For now, First target is make the service alive: like

1. make a sign up page where people can sign up

2. not only sign up, give them their own page to create and manipulate their bio

3. one click resume making extension

4. give user an option to create a blog if she doesn't have one

5. and many more, you can always suggest (open an issue here or mail me.)

Setup
-----

First fork & clone the repo.

I always recommend python-virtualenv for development.

After installing and activating the virtual environment do the follwing

Install the requirements file::

      $ pip install requirements.txt


I am using postgresql-9.1 so you need to install this too::

      $ sudo apt-get install postgresql-9.1

      $ sudo apt-get install postgresql-server-dev-9.1

Now, I spent hours fixing many things on my machine, so I want you don't waste the same.


Setup the database server as follows::

      $ sudo -u postgres createuser <your hostname>

To create the database do this::

      $ sudo -u postgres

      $ sudo createdb aboutmedb 

Now,

      $ sudo -u postgres psql postgres

Enter your sudo password and continue, it will open psql interactive terminal

      $ /password postgres

Enter the password as: postgres

Repeat the password as: postgres

'postgres' is the password without quote

I think your local server is ready to roll now.

cd to aboutme/aboutme locate main.py and run::

      $ python main.py

Happy hacking!

