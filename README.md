# floofpoof

---

How to setup Heroku?

(_Note: you need to install the heroku CLI first_)

- Create a heroku app (for instance from the web interface)
- In your shell, set the "application ID" of your heroku app in a variable (or manually substitute `$appId` by it's value in all the below commands). The application id of an Heroku app is present in the URL of the dashboard. It's also present in the URL of the default `.herokuapp.com` deploy destination.
  - in powershell, use: `$appId="<value>"` (don't forget the quotes `""`)
  - in bash, use: `appId="<value>"` (I didn't test using heroku on bash)
- Then run the commands below

```
heroku buildpacks:clear --app $appId
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git --app $appId
heroku buildpacks:add heroku/python --app $appId
```

- `buildpacks:clear` removes all exisiting buildpacks for the application, giving us a fresh start
- `buildpacks:add` adds a build pack to the list of buildpacks that are to be executed in order
- `python-poetry-buildpack` is because heroku does not _yet_ handle **Poetry** (shame on them! the pull requests have been waiting for allmost 5 months!)
- `heroku/python` is to finally install the python dependencies

Setting up PostGreSQL:

- Add the postgreSQL addon:
  - `heroku addons:create heroku-postgresql:hobby-dev --app $appId`
- Check that it is there by running: `heroku addons`
- (Heroku populates the `DATABASE_URL` environment variable, which can then be consumed by `dj-database-url`)

Note: `psycopg2-binary` is a shadow dependency of Django / PostgreSQL. See:
[Error: No module named psycopg2.extensions](https://stackoverflow.com/a/49308720/9878263)

Adding a superuser:

(follow https://docs.djangoproject.com/en/1.8/intro/tutorial02/)

```
$ heroku run --app $appId -- python manage.py createsuperuser --email=admin@gmail.com
> a
```

Setting up Redis:

```
heroku addons:create heroku-redis:hobby-dev --app $appId
```

Setting daily database backup (time is UTC time) (the minutes must always be `00`):

```
heroku pg:backups:schedule --app $appId --at="12:00"
```
