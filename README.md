# ITeam
The final code of the project is in the last commit of master branch.

In this web application, the third party login is used, which required allauth library. The guide for the installation and preparation is as follow:
1. Run **$ pip install django-allauth** before run the project
2. After running the servers, open http://127.0.0.1:8000/admin with admin super account.
3. open "Sites" and set the default domain name and display name both to http://127.0.0.1:8000
4. Open "social application" and set:
      Provider：GitHub，
      Name：GitHub，
      Client id：9bee54f973940f09c5c0
      Secret key：721621ad19b4625f9f69f626f50a138b5160d8e3
5. Move the site we added before(http://127.0.0.1:8000) from available sites to the right(chosen sites).

