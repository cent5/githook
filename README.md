# Simple auto git pull triggered by repo webhook

## Configure the webhook

You can add webhook(s) by going to the settings page of your online repo.
There are many triggers available to choose from: push, fork, PR created, PR approved, etc.
See specific Git service guides:

* Github: https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks
* Bitbucket: https://support.atlassian.com/bitbucket-cloud/docs/manage-webhooks/

## Configure the listener to perform a git pull on request

1. `git clone https://github.com/cent5/githook.git && cd githook`
2. `cp settings.ini.template settings.ini` then set expected values.
3. Configure nginx. Example:

```
server {
    server_name domain.com;
    location /<WEBHOOK_URL> {
        proxy_pass        http://127.0.0.1:8765/<WEBHOOK_URL>;
        proxy_set_header  X-Real-IP  $remote_addr;
        proxy_redirect off;
    }
    access_log /var/log/nginx/......access.log;
    error_log /var/log/nginx/......error.log;
}
```

4. Setup SSL

5. (A) Use gunicorn to run the listener

```
gunicorn -b 127.0.0.1:8765 server:app --daemon
```

5. (B) Configure systemd service to autostart gunicorn
