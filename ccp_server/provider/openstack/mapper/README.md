# Readme - OpenStack Mapper Class

This Python code provides a MapperClass that can be used to map OpenStack data to Pydantic models.

    async def mapper(resource_name: str, data, cloud: str = None, cloud_type: str = None)

    returns mapped_data

We have created a factory method of Mapper Class named as mapper, which converts the cloud data to the DB model.
It returns mapped data in the form of pydantic model.

There are different cloud Mappers defined in the mapper.yaml file in the mapper module, where left side represents
db model and right side represents the cloud response

A Schema needs to be created after creating map so that we can have control of what is compulsory and has checks on
what fields needs to be inserted into the DB as we will be receiving a lot of chunks from the cloud response.

You need to call mapper() and has to pass the cloud data and the resource name which in your case will be
schemas name. You can additionally pass cloud_type and cloud to the function, but it is not compulsory as it can
fetch which cloud the request was made on and then can fetch the cloud type from the same.
