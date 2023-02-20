import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="snyk_api",
        version="1.0.0",
        description="API for reading and analyzing snyk reports",
        author="Sagi Shumer",
        url="https://github.com/SagiShum/snyk_api_asignment",
        python_requires=">=3.7",
        install_requires=[
            "pygithub"
        ]

    )