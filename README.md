run
# build
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt

# run
# fix django.db.utils.OperationalError: no such column: blog_post.status
python manage.py makemigrations
python manage.py migrate
python manage.py runserver