# Dead Simple Webhookee

## Usage

### Auto git pull

1. `cp settings.ini.template settings.ini` and set expected values.
2. Configure **nginx**. Example:

```
server {
    # TODO: setup SSL
    server_name maybeusesubdomain.domain.com;
    location /<URL_ENDPOINT> {
        proxy_pass        http://127.0.0.1:8765/<URL_ENDPOINT>;
        proxy_set_header  X-Real-IP  $remote_addr;
        proxy_redirect off;
    }
    access_log /var/log/nginx/......access.log;
    error_log /var/log/nginx/......error.log;
}
```

3. Setup SSL
4. Use **gunicorn** to run the listener:

```
gunicorn -b 127.0.0.1:8765 server:app --daemon
```

### Auto git push

In the repo, add a file `.git/hooks/post-commit`:

```bash
#!/bin/sh
git push origin master
```

```shell
chmod +x .git/hooks/post-commit
```

The easiest way to point to the ssh key is to configure it in `~/.ssh/config`, for example:

```
Host bitbucket.org
 HostName bitbucket.org
 IdentityFile ~/.ssh/id_bitbucket
```
