## Dev Challenge

### Local Setup
```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
pip3 install -r requirements.txt
```
- Make a PostgreSQL database, set up the database name with user and password in `DevChallenge/settings.py` under `DATABASES`

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser # create a user 
python3 manage.py runserver
```
---
### APIs
1. Auth
    
`/api/register`

2. Hackathon

