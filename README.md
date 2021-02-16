# DESCRIPTION

This module contains a personal password manager in Python

Initial screen<br>
![Screenshot from 2021-02-15 13-27-18](https://user-images.githubusercontent.com/59267157/107972949-5a40bd80-6f93-11eb-9bd1-cfd41123d1df.png)

Create user screen<br>
![Screenshot from 2021-02-15 13-27-27](https://user-images.githubusercontent.com/59267157/107972954-5b71ea80-6f93-11eb-91a1-48e6469a2e6b.png)

Create credential screen<br>
![Screenshot from 2021-02-15 13-27-58](https://user-images.githubusercontent.com/59267157/107972956-5b71ea80-6f93-11eb-8fce-d1ba76a9c7c9.png)

Registered credentials screen (with encrypted passwords)<br>
![Screenshot from 2021-02-15 13-28-00](https://user-images.githubusercontent.com/59267157/107972959-5c0a8100-6f93-11eb-9f73-198686469185.png)

Registered credentials screen (with decrypted passwords)<br>
![Screenshot from 2021-02-15 13-28-04](https://user-images.githubusercontent.com/59267157/107972961-5c0a8100-6f93-11eb-9762-da6c38818b64.png)

# INSTALLATION

Create a .env file containing the data from .env.example. The database directories should not be changed unless necessary.
It is also required to generate a salt value (follow instructions on .env.example).

## Setting up the environment

Using anaconda environments:
```ignorelang
conda env create -f env.yml
```

Using pipenv
```ignorelang
pip install pipenv
pipenv install
```

# Run

To run the application, simply use the commands below, depending on whether you are using anaconda or pipenv.
All required databases and tables will be created under the "database" directory

Using conda:
```ignorelang
conda activate password_manager
python .
```

Using pipenv:
```ignorelang
pipenv run python .
```