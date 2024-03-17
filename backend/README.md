## How to start the server locally for development

1. CD into the backend directory.

```bash
cd backend
```

2. Install the dependencies by running the following command:

```bash
pip install -r requirements.txt
```

After installing the dependencies, you can start the server by running the following command:

```bash
uvicorn src.main:app --reload
```

or

```bash
python app.py
```

if you want to use the `app.py` file to start the server, make sure to have an `ENV` environment variable set to `development` to enable live reloading. (only for development purposes)

```bash
export ENV=development
```

## API documentation

The API documentation is available at /docs or /redoc after starting the server.
You can access the documentation by visiting the following URL: (use the port number you have set)

```txt
http://localhost:42069/docs
http://localhost:42069/redoc
```
