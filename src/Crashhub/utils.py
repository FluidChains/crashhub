import datetime
import traceback
from contextlib import contextmanager

from flask import current_app as app, g
from .lib import issues, github


def get_greeting():
    now = datetime.datetime.now()
    if now.hour < 12:
        return "Good morning"
    if now.hour < 17:
        return "Good afternoon"
    return "Good evening"


def update_posts(dry_run):
    with g.db('get_all_crashkinds.sql') as cur:
        columns = [desc[0] for desc in cur.description]
        kinds = cur.fetchall()
        kinds = [dict(zip(columns, row)) for row in kinds]

    for k in kinds:
        try:
            if not k.get('github_id'):
                continue
            _, body = issues.format_issue(k.get('id'))
            if not dry_run:
                github.update_issue(k.get('github_id'), body)
            if github.issue_is_closed(k.get('github_id')):
                body = issues.format_reopen_comment(k.get('id'), github.issue_closed_by(k.github_id))
                if body:
                    print("Respond", k.get('github_id'), body)
                    if not dry_run:
                        github.respond(k.get('github_id'), body)
        except:
            traceback.print_exc()