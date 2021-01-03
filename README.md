# Dead Simple Webhookee

## Usage

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