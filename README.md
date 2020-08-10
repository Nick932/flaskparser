# Flask parsing api
A light api, based on Flask.

Parses given uri, collects it's data and pack it to an archive.
Returns a uri to download the archive.

Endpoints:

/parsingapp/api/v1.0/new_task/<url_to_parse> (via POST method) - takes uri to parse.
Returns the id of the bound task.

/parsingapp/api/v1.0/task/<task_id> (via GET method) - takes the id of the task.
Returns the task's status or a uri to download task's result.


# Running
0) PostgreSQL database must be prepared according to the Celery backend settings.
1) In the directory with files, execute 'celery -A views.celery worker' command in the shell's window
2) Then in a separate window, execute 'python run.py'

# Technologies used
- Flask
- Beautiful soup
- PostgreSQL
- Celery

# Requirements
- Python 3.5.2+
- Linux OS (was tested on Ubuntu 16.04)
- See 'requirements.txt' for more details

# To contribute
There are no something special to join the project.

# Contacts
To contact with me: @MaikSturm932 (using Telegram app)
or email: maik.sturm932@gmail.com
