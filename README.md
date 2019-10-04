# Notifico!

Notifico is an open-source relay to deliver notifications to IRC channels.
Notifico works with many 3rd party services such as GitLab and GitHub.

## Installation

### Setup

First, create a virtualenv to keep dependencies self-contained:

    python -m venv notifico-env
    source notifico-env/bin/activate

The virtualenv step can be skipped to install all dependencies globally.
However, this is not recommended, and requires running the following step as
root.

Next, install notifico and all of its dependencies.

    python setup.py install

### Initial configuration

Copy the notifico config file to `local_config.py`

    cp notifico/config.py local_config.py

Edit:

* `SECRET_KEY` - set it to some random long string (you can generate one with,
  e.g. `openssl rand -base64 48`)
* Optional: `NOTIFICO_NEW_USERS` should be set to False for private servers
  **after** having registered one user through the web UI.
* Optional: `NOTIFICO_PASSWORD_RESET`, requires configuring Flask-Mail
  (`MAIL_SERVER`, `MAIL_PORT`, etc)

Initialize the database:

    python -m notifico init

### Starting

The following commands need to be run:

    python -m notifico www         # add "--host 0.0.0.0" to make it public
    python -m notifico bots
    python -m notifico worker      # not needed if password resets are disabled

You can do this in three separate screen/tmux windows, or use the provided
supervisor config in `misc/deploy/supervisord.conf`.

You can now go to `your-server:5000` with a web browser, register and set up
webhooks if you wish, or do the next step to access through port 80.

### Testing

Install the test dependencies with:

    pip install -e ".[tests]"

and then run the tests with:

    pytest

### Nginx proxying

Use the following nginx config to have notifico in a subdomain and have it
handle static files:

    server {
        # change these two
        server_name notifico.example.com;
        root /path/to/notifico/static;

        try_files $uri @notifico;
        location @notifico {
            proxy_pass http://127.0.0.1:5000;
        }
    }

`NOTIFICO_ROUTE_STATIC` can be set to False with this.
