fabric-startproject
===================

Fabric script to create Django project with base structure, virtualenv, settings and urls configuration.

The project was born from a script that I found on django planet and i modified it for
personal use.

In particular it works in Django 1.4 and you can use it in 2 ways:

``fab start_project:project_name``

need to create a structure of folder with simply configuration.

To configure a base admin site, you need isntead to run this one:

``fab start_project:project_name,activate_admin``

Remember to customize a PACKAGES_LIST variable in fabfile, for your personal
use. These are the packages the script will install into the virtualenv.

A parte from this, if you have some ideas, tell me immediately!!!! :)

Credits
=======

Special thanks to the authors of this resources:

https://gist.github.com/2818562