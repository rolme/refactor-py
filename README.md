# Refactor Python

Refactor sample app written in python using poet and cdk

## Requirements

* Python 3.11.x
* poerty 1.6.x

## Installing Poetry

After installing python 3.11.x, make sure to install poetry. NOTE: if you are using `asdf` as a tool manager, DO NOT use `brew` to install.

```sh
curl -sSL https://install.python-poetry.org | python -
```

## Setup

after ensuring you have the correct python and poetry installed, run the following:

```sh
poetry shell
poetry env use $(which python)                 # you can run `poetry env info` to ensure python version matches .tool-versions
poetry config virtualenvs.in-project true
poetry install
```

## Define .env

You will need an [API Key for OpenAI](https://platform.openai.com/account/api-keys). Once you have it, place it in your newly created `.env` file.

```sh
cp .env-example .env
```

## Create an AWS refactor profile

You will need to request an IAM access key and secret. Then run the following command

```sh
aws configure --profile refactor
```

## CDK Python

```sh
cdk synth
cdk --profile refactor bootstrap      # first time, you will need to bootstrap
cdk --profile refactor deploy
```

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

### Database Design
