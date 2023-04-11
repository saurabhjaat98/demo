# CCP - Cirrus Cloud Platform

CCP is a cloud aggregator application that connects with OpenStack, AWS, GCP, and other cloud platforms. The application
allows users to perform cloud-related operations such as managing virtual machines, storage and networks.

### Requirements

- Python version 3.10
- Pip version 22.2
- Docker and Docker Compose
- Environment variables (listed in the next section)

### Running the Application

To run the application, you need to start the required services such as MongoDB and Redis. You can use the provided
docker-compose.yml file to start these services with the following command:

```dockerfile
sudo docker-compose up -d mongo redis
```

To run the CCP application in a container run the following command

```dockerfile
sudo docker-compose up -d
```

Install the dependencies for the application by running the following pip command:

```commandline
pip install -r requirements.txt
```

Start the server by running the following command:

```commandline
uvicorn ccp_server.main:app --reload
```

Run the application using Makfile

```makefile
make run
```

The application is built using FastAPI and the Swagger UI for API documentation is
available [here](http://localhost:8000/docs).

### Clouds Credentials

The cloud credentials are stored in the `clouds.yaml` file, which is provided with the project. If not found
in `/etc/ccp/`, the application will pick the project's clouds.yaml. The file can be accessed
at [clouds.yaml](./clouds.yaml).

It is important to keep the cloud credentials secure and to not share them with unauthorized users.

### Environment Variables

There are some environment variables required to run the project. These environment variables can be found in
the [env_variables.py](./ccp_server/util/env_variables.py) file.

```text
KEYCLOAK_HOST
KEYCLOAK_HOST_PROTOCOL
KEYCLOAK_CLIENT_ID
KEYCLOAK_REALM
KEYCLOAK_CLIENT_SECRET
MONGO_DB_URL
REDIS_URL
LOG_FILE_PATH
```

The default values for these variables are already set in the `env_variables.py` file and you are good to go to run it
on your local machine.

### OpenStack and Keycloak Link

The link for the OpenStack and Keycloak service used by the CCP application can be
found [here](https://coredgeio.atlassian.net/wiki/spaces/CCP20/pages/96829449/OpenStack+and+Keycloak+credentials+for+CCP).

### File Structure

The file structure for the CCP application is as follows:

```text
.
├── ccp_server
│   ├── api
│   │   └── v1
│   │       ├── admin
│   │       ├── compute
│   │       ├── networks
│   │       ├── schema
│   │       └── storage
│   ├── config
│   ├── db
│   ├── decorators
│   ├── files
│   ├── kc
│   │   └── schemas
│   ├── provider
│   │   ├── aws
│   │   ├── gcp
│   │   └── openstack
│   │       ├── compute
│   │       ├── mapper
│   │       │   └── clouds
│   │       ├── network
│   │       └── storage
│   ├── service
│   │   ├── compute
│   │   ├── network
│   │   ├── networks
│   │   └── storage
│   └── util
├── ccp_syncer
├── documentation
└── tests
    ├── compute
    │   └── data
    ├── data
    ├── network
    │   └── data
    └── util
```

### Conclusion

For more documentation, please refer Documentation folder which contains documentation(Readme)
about other flows and functionalities of ccp. [onboarding.md](./documentation/onboarding.md)

CCP is a powerful cloud aggregator application that allows you to manage multiple cloud platforms from a single
interface. With its FastAPI-based API, you can automate and integrate your cloud operations with ease.

For more information about the API and its functionality, please refer to
the [Confluence page](https://coredgeio.atlassian.net/wiki/spaces/CCP20/overview)
