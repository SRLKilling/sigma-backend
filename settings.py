REQUIREMENTS = [

    # Django and DRF related
    "Django == 1.10",
    "djangorestframework == 3.5.3",
    "django-cors-headers == 1.3",
    "django-oauth-toolkit == 0.11",
    "django-filter == 1.0",
    
    # Tornado
    "tornado == 4.4",
    
    # Doc
    "sphinx"
]

PROXY = ''

ENV =  {
    'PYTHON': 'python',
    'PIP': 'pip'
}

PATH = {
    'DJANGO_MANAGER': 'django_app/manage.py',
    'FIXTURES_GENERATOR': 'django_app/generate_fixtures.py',
    'FIXTURES_FILE': 'django_app/fixtures.json'
}
