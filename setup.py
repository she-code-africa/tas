from setuptools import setup, find_packages

setup(
    name='tas',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'gunicorn'
    ]
)
