# Heat Syncer

### Function description

This async function is used to synchronize the stack resources with the mongo db. It takes in a resource_collection_map
which is a dictionary containing the names of stack resources as keys and a list containing the name of the collection
and the function to get the resource as values. It also takes in other parameters such as the cloud, source, cloud_conn,
db_conn_str, and db_name. It fetches all the stack resources, fetches their detailed information,
and syncs them with the mongo db.

#### Parameters

`resource_collection_map`:A Resource Collection Map should have the format below:

{<br>
'Flavor': ['Flavor', 'get_flavor'],<br>
'Image': ['Image', 'get_image'],<br>
'Network': ['Network', 'get_network'],<br>
}<br>
where the key is the name of the stack resource and the value is a list and the
first element of the list is the name of the collection name and the second
element is the function to get the resource.

- `cloud`: The name of the cloud.
- `source`: The source of the cloud data whether it is created by stack or any other source.
- `cloud_conn`:  Connection object of the cloud.
- `db_conn_str`: Connection string of the mongo db.
- `db_name`: Name of the mongo db.

### Return value

This function does not return anything. It just syncs the stack resources with the mongo db.


# Syncer

The SyncResources class is used to synchronize resources from various cloud providers.

It takes func_map argument which includes the mapping of the class and its function to be executed.
The key of the map is the collection name and the value is a list, on which 0 index represents the
service module classes and the 1 index represents the function to be executed.

### Usage

`func_map`
This attribute is a dictionary that maps collection names to a list containing the service module class,
the name of the method to be executed, and the interval in seconds at which to execute the method.
It is used to map collection names to their corresponding classes and methods.

`__init__()`
The constructor for the SyncResources class initializes the __func_map__ dictionary with the appropriate mappings for
the supported cloud resources. The dictionary is used to map the name of the cloud resource collection to the
corresponding class, method that retrieves the resources and the time the resource will get synchronized.

`list_resources`
This method lists the resources of a given class and method. It takes two arguments:

- class_name: the name of the class to be executed
- method_name: the name of the method to be executed

`sync_resources`
This method syncs the resources of a given class and method with a specified collection in the database.
It takes four arguments:

- collection_name: the name of the collection in the database to sync with
- class_name: the name of the class to be executed
- method_name: the name of the method to be executed
- cloud (optional): the name of the cloud provider to sync with

It sets the cloud-id in the ccp_context and then uses the list_resources method to get the resources.
It then uses the SyncerService class to sync the resources with the specified collection in the database.

# Scheduler

The script uses AsyncIOScheduler from apscheduler.schedulers.asyncio to schedule and run periodic tasks to synchronize
resources between different cloud platforms. It also uses ThreadPoolExecutor from apscheduler.executors.pool
for concurrent execution of the scheduled jobs.
