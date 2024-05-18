# Readme

## Start Project
```bash
# pyenv install
python3 -m venv venv
source venv/bin/activate
python manage.py migrate
python manage.py loaddata fixtures/01_base_fixtures
python manage.py runserver

# log in into http://localhost:8000/admin username:admin password:admin
```
## Test with coverage
```bash
coverage run --source='.' manage.py test
```

## Test 2 endpoints
```bash
curl http://localhost:8000/user_contracts_information
curl http://localhost:8000/contracts_in_2020_not_recurrent
```


## Dump data to fixtures
```bash
python manage.py dumpdata --natural-primary \
                          --natural-foreign \
                          --indent 4 \
                          --exclude auth.permission \
                          --exclude contenttypes \
                          --exclude sessions \
                          --exclude admin \
                          -o fixtures/01_base_fixtures.json
```

[Requirements and resolution](./Q&A.md)
