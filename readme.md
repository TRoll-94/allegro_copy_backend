# Ollegro Project

This project allows you to demonstrate the management of various types of users, as well as their interaction in relation to categories, products, sales and purchases

### Installation

1. Clone the repository to your computer:

   *`git clone https://github.com/TRoll-94/ollegro_backend.git`*
2. Go to the project directory:

   *`cd [project_directory]`*

## Running the Project on Windows

1. Run the project by running the command in the terminal:

   *`docker compose -f "docker-compose.yml" -f "docker-compose.dev.yml" --profile dev -p "ollegro_backend-dev" up --build -d`*
2. You can view the logs and check for errors when starting the server using the command:

    *`docker compose -f "docker-compose.yml" -f "docker-compose.dev.yml" --profile dev -p "ollegro_backend-dev" -f logs`*
3. Open the browser and go to the url:

   *`http://localhost:8000/api/schema/swagger-ui/`*
4. To authorize a user, employ the Bearer authentication method by using a token generated through a request to this 
request endpoint with the following data included in the body:
    *`/api/user/token/`*

{
"email": "user@example.com",
"password": "example"
}

   

5. You can stop the server using command:
 
   *docker compose -f "docker-compose.yml" -f "docker-compose.dev.yml" --profile dev -p "ollegro_backend-dev" down*

Additional commands:
1. Exec to backend dev container:
    *docker exec -it ollegro_backend-app-backend sh*
2. Show base command for dev containers:
    *docker compose -f "docker-compose.yml" -f "docker-compose.dev.yml" --profile dev -p "ollegro_backend-dev"*
3. To restart dev containers:
    *docker compose -f "docker-compose.yml" -f "docker-compose.dev.yml" --profile dev -p "ollegro_backend-dev" restart*
--

## Running the Project on Linux
1. Run the project by running the command in the terminal:

   *make dev*
2. You can view the logs and check for errors when starting the server using the command:

   *make dev-logs // make dev-logs backend*
3. To restart the server, use the command:

   *dev-restart*
4. To stop the server, use the command:

   *dev-down*
5. To execute to backend dev container, use the command:

   *make dev-exec*


### Testing

1. Check authorised user data:
   *GET /api/user/*
2. Create a category with a unique code
   *POST /api/products/category/*
3. Check the created category:
    *GET /api/products/category/*
4. Create a new product property with the following parameters:
 ```json
{
  "category": 1,
  "name": "Color blue",
  "code": "color",
  "value": "blue"
}
```
5. Add a new product with the following parameters. Example:
 ```json
{
  "properties": [
    1
  ],
  "name": "VW",
  "description": "das auto",
  "price": "5000",
  "total": 5,
  "total_reserved": 0,
  "sku": "VW passat",
  "category": 1,
  "owner": 0
}

```
6. Buy a product with an ID and an empty body:
   - Conduct a product purchase operation using the identifier and an empty request body.
   buy a product with id and empty body
   - Use link from the response for payment
   - for payment you can use test generated card number 4062 8316 5997 5374

### Requirements

Before running, make sure you have the git version control system and docker are installed in your environment


