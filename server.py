from datetime import datetime
from pathlib import Path

from decouple import config
from flask import Flask, request, Response
from git import Repo

app = Flask(__name__)


URL_ENDPOINT = config('URL_ENDPOINT')
LIGHTWEIGHT_LOG_FILE = config('LIGHTWEIGH_LOG_FILE')
REPO_PATH = config('REPO_PATH')
SSH_CRED = config('SSH_CRED')


@app.route(URL_ENDPOINT, methods=['POST'])
def respond():
  return _handle(request.json)


def _handle(r):
  try:
    latest_commit = r['push']['changes'][0]['commits'][0]['message']
  except (KeyError, IndexError):
    latest_commit = 'N/A'

  with Path(LIGHTWEIGHT_LOG_FILE).open('a') as fout:
    fout.write(f'triggered at {datetime.now().isoformat()}: {latest_commit}')
    repo = Repo(REPO_PATH)
    with repo.git.custom_environment(GIT_SSH_COMMAND=f'ssh -i {SSH_CRED}'):
      o = repo.remotes.origin
      o.pull()
    fout.write('| pulled\n')

  return Response(status=200)
