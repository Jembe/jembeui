# {{project_name}}

{{project_description}}

## Development

To install required development dependencies and prepare development enviroment execute:

```bash
$ pip install -e .[dev]
$ npm install
```

### Start development enviroment
    
To start development web server execute:
```bash
$ flask run
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