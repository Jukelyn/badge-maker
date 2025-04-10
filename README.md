# Workflow Statuses

![Docker Deploy Workflow Badge](https://github.com/Jukelyn/badge-maker/actions/workflows/docker-deploy.yaml/badge.svg)
![CI-SFTP Workflow Badge](https://github.com/Jukelyn/badge-maker/actions/workflows/ci-sftp.yaml/badge.svg)

## Table of Contents

- [Introduction](#introduction)
- [Local Development](#local-development)
- [Deployment Workflows](#deployment-workflows)
  - [Workflow Actions Secrets](#workflow-actions-secrets)
  - [CI-SFTP Workflow](#ci-sftp-workflow)
  - [Docker Deploy Workflow](#docker-deploy-workflow)

# Introduction
The frontend of this web application is built with Next.JS (React) and TypeScript, while the backend utilizes Python's Flask framework. The input area can recieve comma seperated simpleicons slugs. All the available valid slugs can be found [here](https://badge-maker-api.jukelyn.com/available_icons). The outputted badges are made to used in markdown enviornments but since the url is in the output, that can be easily extracted and used in other places as well.

# Local Development

First, run the Python API:

```bash
$ python3 -m venv api/venv
$ source api/venv/bin/activate
$ pip install --upgrade pip  # (optional)
$ pip install -r api/requirements.txt
$ python api/run.py
```

then, run the development (frontend) server:

```bash
$ npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

# Deployment Workflows

There are two [workflows](https://docs.github.com/en/actions/writing-workflows/about-workflows) that I have written (`ci-sftp.yaml` and `docker-deploy.yaml`) that will automatically copy files from the repo to a server and use docker compose to deploy containers for the API and frontend.

### Workflow Actions Secrets
In order for the workflows to work, there needs to be 5 repository secrets set. Here are some examples of what those are and example values:

```yaml
REMOTE_PATH = "/home/user/git_repos/repo/"
SSH_SERVER = "domain.tld"
SSH_SERVER_PORT = 12345
SSH_USER = "user"
```

The last one is the `SSH_PRIVATE_KEY`. For this one, you need to generate a SSH key pair for your server. You can re-use a key that you already have or make a new one just for this workflow. 

<details><summary>Creating an SSH Key Pair</summary>
Here's how you would create a SSH key pair:

```bash
$ ssh-keygen -t rsa -b 4096 -f ~/.ssh/example  # On your local machine
$ ssh-copy-id -i ~/.ssh/example [USER]@[SERVER IP OR DOMAIN]  # Copies the key to the server
```

</details>

<details><summary>Example RSA Private Key</summary>

```bash
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAMxovdzKkOsXrIs69c1SaaEM0aFlQjBf8MFwEYoyKAnzYstjUH+j
wiTCQynKG5HUzwMISeRiocDoAzA19wFsgj0CAwEAAQJAFQiOHjhl3cW2MS7O+OK1
uycOMcpb8OMJFg6JxNZREmeJfoK5SoOQtRr7m1IDhdwJZKk+tQUCSFnzzJMjtfgF
jQIhAPGr90xleWdHSwZpA21wudnRfqQwkkBPKNBIyG9O4wYPAiEA2Ic2kt3WXOo1
EZEMKx2+UnBDjmjGWOojqii/1R9IHvMCIQCyxeNKQEZuf+6f7075xkm1N6PXEZce
u3AVo8GhlVmbQQIhALOFZ3nc8x2WEOm/mJcm0eUHrvsjY0/U0D0EDAhnJySBAiBb
zqzMjrgHcYIto69BD1iD+aASfhGM4PdXD5lxrM/G8A==
-----END RSA PRIVATE KEY-----
(leave newline here)
```

Read [this](https://jukelyn.com/posts/ssh-keys/) for more info on SSH keys.

</details>

Once you have the SSH public key on the server copy the contents of the *private* key to the `SSH_PRIVATE_KEY` repository secret. Don't forget the newline at the end.

## CI-SFTP Workflow
The `CI-SFTP.yaml` workflow uses the SFTP-Deploy-Action from wlixcc. The workflow has one job that runs on a Linux server provided by GitHub. First, it downloads the code. It then copies all the files from your project to a specific folder on the server (specified by `REMOTE_PATH` and `SSH_SERVER`), and it first deletes everything that's already in that folder on the server. It also sets a short time limit for connecting to the server.

## Docker Deploy Workflow

The `docker-deploy.yaml` uses the `docker compose` command so make sure that the server you are pushing to has the Docker Engine, CLI, and compose plugin. See [here](https://docs.docker.com/compose/install/#scenario-two-install-the-docker-compose-plugin) for more info on installing Docker (compose). It connects to the remote server using SSH with a private key stored securely as a secret. Once connected, it navigates to a specific directory and runs `docker compose up --build -d`. This command rebuilds the Docker images if needed and then starts or updates the containers defined in the `docker-compose.yaml` file on the server. Finally, it cleans up by deleting the temporary private key file from the workflow runner.
