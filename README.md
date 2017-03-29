# Try Django upload file

1. 使用django model 的manager來將上傳的檔案做chunks並且產生md5

# Setup

1. Source virtualenv

2. `pip install -r requirement.txt`

3. `python manage.py migrate`

4. `python manage.py runserver`

5. open browser to 127.0.0.1:8000

6. try to upload file then use sqliteman to check DB.

