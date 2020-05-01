# Crashhub/db/db.py
import logging

import click
from flask import current_app, g
from flask.cli import with_appcontext

from .db_context import DatabaseContext

logger = logging.getLogger(__name__)

def get_db():
    if 'db_context' not in g:
        g.db_context = DatabaseContext(current_app.config['POSTGRES'])
    return g.db_context
    
def close_db():
    db_context = g.pop('db_context', None)
    if db_context is not None:
        db_context.close_connection()

class DatabaseManager:

    def __init__(self, connection, root):
        self.conn = connection
        self.root = root
        
    def __call__(self, query, cursor_factory=None, **params):
        self.cur = self.conn.cursor(cursor_factory=cursor_factory)
        try:
            with current_app.open_resource(self.root+query) as f:
                self.cur.execute(f.read().decode('utf-8'), params)
        except Exception as e:
            logger.exception(query)
            print(params)
        else:
            return self

    def commit(self):
        self.conn.commit()
        return self

    def close(self):
        self.cur.close()
        return self

    def __enter__(self):
        return self.cur

    def __exit__(self, exception_type, exception_value, traceback):
        self.cur.close()
        if exception_type:
            print(exception_type, exception_value)
            print(traceback)

def init_db():
    db = get_db().return_connection()
    cur = db.cursor()
    with current_app.open_resource('db/sql/schema.sql') as f:
        cur.execute(f.read().decode('utf-8'))
        db.commit()
        close_db()

@click.command('init-db', short_help='Initialize database.')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized database')

def init_app(app):
    app.cli.add_command(init_db_command)