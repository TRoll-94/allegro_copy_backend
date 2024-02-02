# Ollegro Project

This project allows you to demonstrate the management of various types of users, as well as their interaction in relation to categories, products, sales and purchases

### Installation

1. Clone the repository to your computer:

   *git clone https://github.com/TRoll-94/ollegro_backend.git*
2. Go to the project directory:

   *cd [project_directory]*

## Running the Project on Windows

1. Run the project by running the command in the terminal:

   *docker compose -f "docker-compose.yml" -f "docker-compose.dev.yml" --profile dev -p "ollegro_backend-dev" up --build -d*
2. You can view the logs and check for errors when starting the server using the command:

    *docker compose -f "docker-compose.yml" -f "docker-compose.dev.yml" --profile dev -p "ollegro_backend-dev" -f logs*
3. Open the browser and go to the url:

   *http://localhost:8000/api/schema/swagger-ui/*
4. You must authorise user via cookieAuth (apiKey) using a token
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

### Requirements

Before running, make sure you have the git version control system is installed in your environment


