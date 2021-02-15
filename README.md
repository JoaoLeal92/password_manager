# DESCRIPTION

This module contains a personal password manager in Python

# INSTALLATION

This password manager was developed using anaconda environments. 

Creating environment
```ignorelang
conda env create -f env.yml
conda activate password_manager
```

Create a .env file containing the data from .env.example. The database directories should not be changed unless necessary.
It is also required to generate a salt value (follow instructions on .env.example).

# Run

To run the application, simply use the command below.
All required databases and tables will be created under the "database" directory
```ignorelang
python .
```
