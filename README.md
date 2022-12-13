
# Yatube
## This is a Yatube project - small social network. The goal of the project is to explore the capabilities of the Django REST framework.<br>
Implemented API functionality for a small social network.<br>
Users can:
 - register
 - create posts
 - leave comments on posts
 - subscribe to favorite authors

### Project run:


```
git clone https://github.com/yandex-praktikum/kittygram.git
```

```
cd api_final_yatube/yatube_api
```

```
python3 -m venv env
```

```
source env/bin/activate
```


```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

```
python3 manage.py migrate
```


```
python3 manage.py runserver
```