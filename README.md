### Fastapi Users module
---
This is module contains User CRUD operations and login api. You can add this users directory directly in any other project to get users api end points ready by just copy and past user directory and add it in routes. 

### How to run this.
---   
1. Set up .env file with following keys.Set values as per your requirement
````
SECRET_KEY=xxxx #this is for encryption of token
DATABASE_URL=postgresql://postgres:postgres@localhost/loginmodule
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_NAME=loginmodule
DATABASE_PORT=5432
````
2. Install dependenceny   
````
pip install -r requirements.txt
````
3. Run the below command to start fastapi
````
uvicorn main:app --reload
````
4. You can see api swagger here [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)