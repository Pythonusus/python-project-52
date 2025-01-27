<div align="center">

<img src="https://i.imgur.com/vNVgzzO.png" alt="Task manager logo" width="300" height="300">

# Task manager

### Maintainability, tests and test coverage status:
[![Actions Status](https://github.com/Pythonusus/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pythonusus/python-project-52/actions)
[![Actions Status](https://github.com/Pythonusus/python-project-52/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Pythonusus/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/97261c1c623317d016f2/maintainability)](https://codeclimate.com/github/Pythonusus/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/97261c1c623317d016f2/test_coverage)](https://codeclimate.com/github/Pythonusus/python-project-52/test_coverage)

</div>

## 🔗 Link to web-service
[Try Task manager by this link](https://task-manager-9oao.onrender.com)

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Built Using](#built_using)
- [Authors](#authors)
- [Logo](#logo)

<a name = "about"></a>
## 🧐 About

Simple task manager for life

<a name = "getting_started"></a>
## 🏁 Getting Started

### Prerequisites

1. python = "^3.12"
2. poetry = "^1.8.5"

### Installing

1. Clone GitHub repo:
```
git clone https://github.com/Pythonusus/python-project-52
```

2. Provide SECRET_KEY environmental variable to secure your data:
```
export SECRET_KEY=yourveryhardtobreakpassword
```

3. Provide DATABASE_URL environmental variable if you want to use database other than default sqlite3:
```
export DATABASE_URL={provider}://{user}:{password}@{host}:{port}/{db}
```

4. Install all neccessary dependencies using Poetry:
```
make build
```

5. Start Task Manager locally:
```
make start
```

<a name = "built_using"></a>
## ⛏️ Built Using

- [Poetry](https://python-poetry.org) - Python packaging and dependency management tool
- [Django](https://www.djangoproject.com/) - high-level Python web framework
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP Server for UNIX
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [WhiteNoise](https://whitenoise.readthedocs.io/en/latest/) - simplified static file serving for Python web apps
- [dj-database-url](https://pypi.org/project/dj-database-url/) - database URL configuration for Django
- [python-dotenv](https://pypi.org/project/python-dotenv/) - manage environment variables
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) - PostgreSQL database adapter
- [django-extensions](https://pypi.org/project/django-extensions/) - useful extensions for Django
- [django-filter](https://pypi.org/project/django-filter/) - reusable Django application that allows users to filter querysets dynamically
- [rollbar](https://pypi.org/project/rollbar/) - real-time error monitoring and reporting tool
- [flake8](https://pypi.org/project/flake8/) - tool for style guide enforcement
- [pylint](https://pypi.org/project/pylint/) - static type checker and code analyzer
- [factory-boy](https://pypi.org/project/factory-boy/) - factory and fixture emulation for testing
- [coverage](https://pypi.org/project/coverage/) - code coverage measurement for Python


<a name = "authors"></a>
## ✍️ Authors

[@Pythonusus](https://github.com/Pythonusus)

<a name = "logo"></a>
## Logo
Made with [Ideogram AI](https://ideogram.ai/)

Stored at [imgur.com](https://imgur.com/)
