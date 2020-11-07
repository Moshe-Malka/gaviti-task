# "Gaviti" Exam/Task

This is my code for the task.
it uses Flask, PyMongo and Celery to serve 2 endpoints:
- POST /search => allows to search for records in a local MongoDB by 2 fields, 'startDate' and 'endDate'. the results of the query are saved locally and the response is a link to download the local file with the results.
- GET /download/<filename> => get specific file by the filename (excluding file format). response is the content of file.

## Dependencies
You would need Python 3.X installed on your computer to use this.

## Setup

### Clone this repo
```bash
git clone https://github.com/Moshe-Malka/gaviti-task.git
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip3 install -r requirements.txt
```
### MongoDB
Download and install [MongoDB](https://www.mongodb.com/try/download/community)
you can create dummy data using [Mockaroo](https://www.mockaroo.com/) and then import that data to MongoDB using the command:
```bash
mongoimport --db <name_of_your_db> --collection <name_of_your_collection> --drop --file <json_file_path>
```
`NOTE`: make sure the data has a field called "timestamp" and it contains a unix timetampe integer (long).

### Redis
Download and install [Redis](https://redis.io/topics/quickstart)

## Usage
1) run the mongodb service:
Mac:
```brew services start mongodb```
Windows:
```mongod```

2) run the redis service:
Mac:
```redis-server```
Windows:
```redis-server.exe```

3)run the flask app:
```python3 main.app```

you can test it using cUrl or postman.