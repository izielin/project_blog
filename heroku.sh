project_dir=$PWD
cd $project_dir
source venv/bin/activate
heroku login
cd $project_dir
cat > Procfile < EOF
web: gunicorn project_blog.wsgi --log-file -
EOF
cat > runtime.txt < EOF
python-3.7.3
EOF


# set venv
sudo apt install libpq-dev python3-dev
pip install gunicorn psycopg2 whitenoise dj-database-url
pip freeze > requirements.txt
