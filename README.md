# jclub

Django based journal club lab meeting organizer.


## Copyright 

Copyright 2014--2015
* Alex Seeholzer <alex.seeholzer@epfl.ch>
* Friedemann Zenke <friedemann.zenke@epfl.ch>

JClub is released under the GPLv2 (please see LICENSE).


## First start

To set up, first run:
`python manage.py migrate`

Then to set up a superuser
`python manage.py createsuperuser`

And finally to run the test server 
`python manage.py runserver`

This will start the test server to respond only to local host, 
to respond to external requests run
`python manage.py runserver 0.0.0.0:8000`


##  Todo
- [ ] allow user self-editing
- [ ] add tequila authentication
