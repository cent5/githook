from datetime import datetime
import logging

from decouple import config
from flask import Flask, request, Response
from git import Repo

logging.basicConfig(filename=config('LOG_FILE'),
                    level=logging.INFO,
                    force=True)

REF_MASTER_BRANCH = 'refs/heads/master'


app = Flask(__name__)


@app.route(config('WEBHOOK_URL'), methods=['POST'])
def respond():
  r = request.json
  commit_info = _read_commit_info(r)
  logging.info(f'Triggered at {datetime.now().isoformat()}: {commit_info}')
  if not commit_info['is_master']:
    return Response(status=200)

  if config('REPO_PATH'):
    repo = Repo(config('REPO_PATH'))
    with repo.git.custom_environment(GIT_SSH_COMMAND=f"ssh -i {config('SSH_CRED')}"):
      o = repo.remotes.origin
      o.pull()
    logging.info('\-pulled')
  else:
    logging.warning('\-missing REPO_PATH config')

  return Response(status=200)


def _read_commit_info(r):
  log_msg = {'pusher': None, 'commit_msg': None, 'is_master': False}
  if config('WEBHOOK_SOURCE').lower() == 'bitbucket':
    try:
      log_msg['commit_msg'] = r['push']['changes'][0]['commits'][0]['message']
    except (TypeError, KeyError, IndexError):
      pass
  else:
    # Default to Github webhook
    log_msg['is_master'] = r['ref'] == REF_MASTER_BRANCH
    if 'head_commit' in r:
      log_msg['commit_msg'] = r['head_commit']['message']
    else:
      log_msg['commit_msg'] = r
    if 'pusher' in r:
      log_msg['pusher'] = r['pusher']['name']
  return log_msg