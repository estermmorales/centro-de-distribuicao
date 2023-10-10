### Centro de distribuição

Sistema para gerenciamento de entrega e retirada de pacotes.

Para rodar localmente:

1. Crie um ambiente virtual

```
python -m venv venv
```

2. Ative-o

```
venv\Scripts\activate      //Windows
source venv/bin/activate   //Linux
```

3. Instale as depêndencias do projeto

```
pip install -r requirements.txt
```

4. Configure um arquivo mysql.cnf com as informações do seu banco de dados local

```
[client]
database = your_database
host = localhost
user = your_user
password = your_password
default-character-set = utf8
```

5. Faças as migrações e rode \o/

```
python manage.py migrate
python manage.py runserver
```
