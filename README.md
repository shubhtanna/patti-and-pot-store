# Patti & Pot

Online store for Patti & Pot, a small tea house in Pune selling estate-direct Assam, Darjeeling and
Nilgiri teas, chai blends and teaware.

Built with Django 5.2 (server-rendered templates, SQLite). The range is loaded by a data migration
from `shop/catalog.py`; the cart lives in the visitor's (signed cookie) session.

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Deployed on Render: build `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`,
start `gunicorn pattipot.wsgi`.

Demo store: no real orders, payments or deliveries.
