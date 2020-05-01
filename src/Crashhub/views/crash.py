# Crashhub/views/crash.py
import datetime
import json
import os
import logging

from flask import Blueprint, request, current_app as app, g

from . import bp_crash
from ..db.db import get_db, close_db, DatabaseManager

from ..lib import issues, github

from werkzeug.local import LocalProxy
db_context = LocalProxy(get_db)

logger = logging.getLogger(__name__)

@bp_crash.before_request
def before_request():
    try:
        conn = db_context.return_connection()
        g.db = DatabaseManager(conn, 'db/sql/')
    except Exception as e:
        logger.exception('before_request')

@bp_crash.after_request
def after_request(response):
    return response

@bp_crash.route('/test', methods=['GET'])
def test():
     return '<h1>TEST SUCCESS</h1>'

@bp_crash.route('/crash', methods=['POST'])
def store_crash_legacy():
    response = store_crash(request)
    if response["status"] != "reported":
        return response["text"]
    else:
        return response["text"].replace("GitHub",
                                        """<a href="{}">GitHub</a>""".format(response["location"]))

@bp_crash.route('/crash.json', methods=['POST'])
def store_crash_v2():
    return json.dumps(store_crash(request))


def store_crash(request):
    if not check_rate_limit(request):
        return {
            "text": "Thanks for reporting this issue!",
            "status": "skip",
            "location": None
        }

    crash = json.loads(request.data)
    # Give Windows paths forward slashes
    crash["id"]["file"] = crash["id"]["file"].replace("\\", "/")
    # We only care about the file name
    crash["id"]["file"] = os.path.split(crash["id"]["file"])[1]

    with g.db('get_crashkind.sql', **crash['id']) as cur:
        columns = [desc[0] for desc in cur.description]
        kind = cur.fetchone()
    if not kind:
        with g.db('new_crashkind.sql', **crash['id']) as cur:
            columns = [desc[0] for desc in cur.description]
            kind = cur.fetchone()
        g.db.commit()
    
    del crash["id"]
    crash["kind_id"] = kind.id
    g.db('new_crash.sql', **crash).close().commit()
    
    title, body = issues.format_issue(kind.id)
    if kind.github_id < 0:
        issue = github.report_issue(title, body)
        g.db('update_crashkind_github_id.sql', id=kind.id, github_id=issue).close().commit()
    else:
        github.update_issue(kind.github_id, body)
        if github.issue_is_closed(kind.github_id):
            body = issues.format_reopen_comment(kind.id, github.issue_closed_by(kind.github_id))
            print(body)
            if body:
                print("body", body)
                github.respond(kind.github_id, body)
    url = "https://github.com/{}/issues/{}".format(app.config.get("GITHUB_PROJECT"), kind.github_id)
    return {
        "text": "Thanks for reporting this issue! You can track further progress on GitHub.",
        "status": "reported",
        "location": url
    }

def check_rate_limit(request):
    ip = request.remote_addr
    g.db('new_logentry.sql', sender_ip=ip).close().commit()
    with g.db('count_logentry_ip.sql', sender_ip=ip) as cur:
        num_requests = cur.fetchone()[0]
    return num_requests < 4
