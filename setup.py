import setuptools

setuptools.setup(
    name="ccp_server",
    version="1.0.0",
    author="Coredge.io India Pvt Ltd.",
    url="www.coredge.io",
    author_email="info@coredge.io",
    description="CCP API Server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Proprietary",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    package_data={
        "": ["provider/openstack/mapper/clouds/*.yaml", "files/*"]},
    python_requires=">=3.10"
)
