# {{project_name}}

{{project_description}}

## Development

To install required development dependencies and prepare development enviroment execute:

```bash
$ pip install -e .[dev]
$ npm install
$ flask db upgrade
```

### Configuration
If on your local development computer you have:

- postgres then just create `{{ project_name }}` database in it.
- redis server, leave it as it is, app will use it for sessions and caching.

Othervise you need to open `instance/config.py` configuration file and configure
connection to your postgres database and redis server for caching.

### Start development enviroment
    
To start development web server execute:
```bash
$ flask run
```
To redis queue worker execute:
```bash
$ flask run_rq
```

To watch and build javascript and css during development execute:
```bash
$ npm run dev
```

## Production 

To package project for deployment run:
```bash
$ npm run build
$ python -m build
```