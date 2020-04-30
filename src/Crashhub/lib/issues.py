from distutils.version import LooseVersion

from flask import current_app as app, g

from ..utils import get_greeting

template = """
Crash Report
============

This crash report was reported through the automatic crash reporting system 🤖

Traceback
--------------

```Python traceback
{stack}
{type}: {exc_string}
```

Reporter
------------

This issue was reported by {user_count} user(s):

| {app_name} Version  | Python Version | Operating System  | Wallet Type  | Locale |
|---|---|---|---|---|
{reporter_table}

Additional Information
------------------------

"""

reporter_row = """| {app_version}  | {python_version} | {os} | {wallet_type} | {locale} |
"""

no_info = "The reporting user(s) did not provide additional information."

template_reopen = """
{greeting} @{user_closed},

I just received another crash report related to this issue. The crash occured on {app_name} {version}.
I'm not sure which versions of {app_name} include the fix but this is the first report from anything
newer than {min_version} since you closed the issue.

Could you please check if this issue really is resolved? Here is the traceback that I just collected:

```Python traceback
{stack}
{type}: {exc_string}
```


~ _With robotic wishes_
"""


def format_issue(kind_id):
    with g.db('get_crashkind_by_id.sql', id=kind_id) as cur:
        columns = [desc[0] for desc in cur.description]
        kind = cur.fetchone()
        kind = dict(zip(columns, kind))
    with g.db('get_crashes_by_kind.sql', kind_id=kind_id) as cur:
        columns = [desc[0] for desc in cur.description]
        crashes = cur.fetchall()
        crashes = [dict(zip(columns, row)) for row in crashes]

    reporter_table = ""
    additional = []
    for c in crashes:
        reporter_table += reporter_row.format(**c).replace("\n", " ") + "\n"
        if c.get('description'):
            additional.append(c.get('description'))
    v = {
        "stack": crashes[0].get('stack'),
        "type": kind.get('type'),
        "exc_string": crashes[0].get('exc_string'),
        "reporter_table": reporter_table,
        "user_count": len(crashes),
        "app_name": app.config.get('APP_NAME')
    }
    report = template.format(**v)
    if additional:
        for a in additional:
            report += "\n> ".join([""] + a.splitlines())
            report += "\n\n---\n\n"
    else:
        report += no_info
    title = kind.get('type') + ": " + crashes[0].get('exc_string')
    if len(title) > 400:
        title = title[:400] + "..."
    return title, report


def format_reopen_comment(kind_id, closed_by):
    with g.db('get_crashkind_by_id.sql', id=kind_id) as cur:
        columns = [desc[0] for desc in cur.description]
        kind = cur.fetchone()
        kind = dict(zip(columns, kind))

    with g.db('get_crashes_by_kind.sql', kind_id=kind_id) as cur:
        columns = [desc[0] for desc in cur.description]
        crashes = cur.fetchall()
        crashes = [dict(zip(columns, row)) for row in crashes]

    if len(crashes) < 2:
        return None

    crashes, new_crash = crashes[:-1], crashes[-1:][0]
    min_version = None

    for c in crashes:
        if not min_version or LooseVersion(min_version) < LooseVersion(c.get('app_version')):
            min_version = c.get('app_version')

    if not LooseVersion(min_version) < LooseVersion(new_crash.get('app_version')):
        return None

    v = {
        "greeting": get_greeting(),
        "user_closed": closed_by.login,
        "app_name": app.config.get('APP_NAME'),
        "version": new_crash.get('app_version'),
        "min_version": min_version,
        "stack": new_crash.get('stack'),
        "type": kind.get('type'),
        "exc_string": new_crash.get('exc_string')
    }
    return template_reopen.format(**v)
