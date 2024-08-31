
Build the Docker Image: Run the following command to build the Docker image:

docker build -t fastapi-app .

Run the Docker Container: Use this command to run the container:

docker run -p 8000:80 fastapi-app