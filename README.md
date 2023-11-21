# GLM Model Deployment with FastAPI, Docker, Kubernetes, and GitLab

## Overview

This project demonstrates the deployment of a Generalized Linear Model (GLM) using the FastAPI framework, Docker containers, Kubernetes orchestration, and GitLab for Continuous Integration/Continuous Deployment (CI/CD). The GLM model is served as a web API, providing predictions based on input data.

## Project Structure

- `app/`: Contains the FastAPI application code.
- `app/model/`: Holds the pre-trained GLM model (pickle file).
- `docker/`: Contains Dockerfile for building the Docker image.
- `kubernetes/`: Includes Kubernetes deployment and service YAML files.
- `tests/`: Holds unit tests for the FastAPI application.
- `gitlab-ci.yml`: GitLab CI/CD pipeline configuration file.
- `README.md`: This documentation file.

## Getting Started

1. Clone this repository:
```console
$ git clone https://github.com/ZCai25/glm-fastapi-app.git
```
   
2. Navigate to the project directory:
```console
$ cd glm-fastapi-app
```
3. Follow the instructions in each directory to deploy the GLM model locally or in a Kubernetes cluster.

## End-to-End Process

1. **FastAPI Application:**
   - The FastAPI application (`app/main.py`) defines API endpoints for model prediction.
   - Input data is received via HTTP requests and passed to the pre-trained GLM model.
   - To start the FastAPI server locally, change directory to app and run
     ```console
     $ uvicorn main:app --reload
     ```
   - open [FastAPI Swagger UI](http://localhost:1313/docs) in a browser, which provide a interactive API documenation and exploration web user interfaces.
   - Click "Try it out" at POST/predict and you can test out the model predictions by pasting the data to the request body or upload a file at POST/uploadfile. You can test the output without typing the curl command manually
   ![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/5220d4e6-2386-4e29-9f71-47df2f951ae3)![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/85414d90-f175-4260-abfd-1d15dd083370)![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/d2b66cf2-c7eb-4a0d-9903-f61d7fda54f9)


   - Check out the documenation at [Swagger UI Docs](https://fastapi.tiangolo.com/features/)
2. **Model Loading:**
   - The pre-trained GLM model is stored in the `model/` directory.
   - The model is loaded during the FastAPI application startup.

3. **Docker Containerization:**
   - The Dockerfile (`docker/Dockerfile`) specifies the environment and dependencies for running the FastAPI application.
   - Docker image is built using the `docker build` command, then you can build by running the `run_api.sh`
      - From the project directory, build the container with tag
        ```console
        $ docker build -t glm-fast-api:1.0 .
        ```
      - Make sure the script has execute permissions by running
        ```console
        $ chmod +x run_api.sh
        ```
      - Run the scipt to run the container by typing
        ```console
        $ ./run_api.sh 1313:80
        ```
        you will see the api server started, you can access the server document at (http://localhost:1313/docs)
![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/d217a7e9-2994-4274-9325-840bcb33f42c)


4. **Orchestration:**
   - Orchestration using Docker compose
      - To run the docker compose, change directory to project directory, run
        ```console
        $ docker-compose up
        ```
        It start building docker container using the image`glm-fastapi-app`and run at port 1313 and map to port 80 for the container
     ![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/f8d5739e-7631-4cde-88d7-f8b046fed69a)

      - To stop the service, run
        ```
        $ docker-compose down
        ```
   - Orestration Using Kubernetes
      - Kubernetes deployment YAML (`kubernetes/deployment.yml`) defines how the FastAPI application should run as pods.
      - Kubernetes service YAML (`kubernetes/service.yml`) exposes the application within the cluster.
      - To start the orchestration process locally, start minikube by running
        ```console
        $ minikube start
        ```
        ![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/98649748-9167-420b-b4f3-9df6ba92a3d8)
      - To deploy the resources defined in your deployment.yaml file to a Kubernetes cluster, you can use the kubectl command-line tool. Here are the steps to deploy these resources:
        ```console
           $ kubectl apply -f deployment.yaml
           ```
           This will create the deployment and start the specified number of replicas.

      - Check list deployment running
        ```console
        $ kubectl get deployments
        ```
      - Check pod by running
        ```console
        $ kubectl get pod
        ```
      - Check services by running
        ```console
        $ kubectl get services
        ```
      - Here is a example of the output of the above commands, you can see we create 3 replica in the pod and we deploy them as load balancer to handle large amount of requests![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/b044c916-bbfd-4095-b9a6-fd7d9634d50a)



6. **GitLab CI/CD Pipeline:**
   - `.gitlab-ci.yml` contains the CI/CD pipeline configuration.
   - The pipeline includes stages for linting, testing, building the Docker image, and deploying to Kubernetes.
   - To use this CI/CD configuration, make sure you have GitLab CI/CD configured for your repository, and the necessary variables (e.g., Docker registry credentials) are set in your GitLab project settings.

   - When you push changes to the master branch, GitLab CI/CD will automatically trigger the pipeline, and it will execute the defined stages. The Docker image will be built, pushed to the registry, and then the application will be deployed to Kubernetes.

7. **CI/CD Workflow:**
   - Code changes trigger the GitLab CI/CD pipeline.
   - Automated testing ensures code quality.
   - Docker image is built and pushed to the container registry.
   - Kubernetes deployment is updated with the new image.

## Unit Test & Performance Test
1. **Unit Test**
   - pytest: change directory to test/pytest and run command
     ```console
     $ pytest
     ```
     it will run the `test_main.py` for unit test and `test_requests` for batch test
2. **Performance Test**
   - locust: change directory to test/locust and run command 'locust -f locust_test.py', it will open a server at (http://127.0.0.1:8089/). You can specify the test load and it can output the performance test report.
   - See detail documentation at [this medium post](https://medium.com/@ashmi_banerjee/3-step-tutorial-to-performance-test-ml-serving-apis-using-locust-and-fastapi-40e6cc580adc)
   - Testing Result (see detail reports in the test/locust/report)
     - 10000 users with 10 users request per sec in 60 sec using single api port![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/4378d18b-fc86-4b19-8c32-b7f3f0c49438)
![total_requests_per_second_1313](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/759630a0-1a94-4c83-ac66-c2ce54adfb74)![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/59527029-db71-4afa-811c-713ace346c17)

     - 10000 users with 10 users request per sec in 60 sec using 3 api replicas
     ![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/6737ab74-6c2c-4a26-bca7-490acdb0fc75)![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/913018c9-727f-41e9-a69c-65d3ef3ceb40)![image](https://github.com/ZCai25/glm-fastapi-app/assets/108997562/6f4d1321-2fef-493e-b844-ffe33dfe1d6b)
   - We can see that using 3 replicas balance the load for large amount of request there for total request per second is lower. When the number of request per sec increase to 100, single api port cannot process them and return error, while the 3 replicas and process them. This is a example of testing a api performance test.
  
## 

## Notes

- Update configuration files (`docker/Dockerfile`, `kubernetes/deployment.yml`) based on your model and requirements.
- Adjust GitLab CI/CD settings and environment variables in the GitLab project.

Feel free to explore the project directories for detailed instructions and customization options.
