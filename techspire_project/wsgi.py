"""
WSGI config for techspire_project.
"""
import os
import sys
import shutil
import traceback
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techspire_project.settings')

def ensure_sqlite_db():
    if os.environ.get('DATABASE_URL'):
        return
    try:
        dest_db = Path('/tmp/db.sqlite3')
        candidates = [
            Path(__file__).resolve().parent.parent / 'db.sqlite3',
            Path.cwd() / 'db.sqlite3',
            Path('/var/task/db.sqlite3'),
            Path('/var/task/user/db.sqlite3'),
        ]
        best_src = None
        best_size = 0
        for src in candidates:
            if src.exists() and src.stat().st_size > best_size:
                best_src = src
                best_size = src.stat().st_size

        if best_src:
            dest_size = dest_db.stat().st_size if dest_db.exists() else 0
            if dest_size != best_size:
                shutil.copy2(best_src, dest_db)

        if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
            import django
            django.setup()
            from django.core.management import call_command
            try:
                call_command('migrate', interactive=False)
            except Exception as mig_err:
                print(f"Serverless auto-migration notice: {mig_err}", file=sys.stderr)
    except Exception as e:
        print(f"Notice during db setup: {e}", file=sys.stderr)

ensure_sqlite_db()

try:
    application = get_wsgi_application()
except Exception as init_err:
    init_tb = traceback.format_exc()
    print("FATAL DJANGO INITIALIZATION ERROR:\n", init_tb, file=sys.stderr)
    def application(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        html = f"""<!DOCTYPE html><html><body style="background:#111827;color:#f87171;font-family:monospace;padding:2rem;">
        <h2>Django Initialization Failed:</h2><pre style="background:#1f2937;color:#fca5a5;padding:1rem;border-radius:8px;overflow:auto;">{init_tb}</pre>
        </body></html>"""
        return [html.encode('utf-8')]

def app(environ, start_response):
    try:
        return application(environ, start_response)
    except Exception as req_err:
        req_tb = traceback.format_exc()
        print("FATAL DJANGO REQUEST ERROR:\n", req_tb, file=sys.stderr)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        html = f"""<!DOCTYPE html><html><body style="background:#111827;color:#f87171;font-family:monospace;padding:2rem;">
        <h2>Django Runtime Error:</h2><pre style="background:#1f2937;color:#fca5a5;padding:1rem;border-radius:8px;overflow:auto;">{req_tb}</pre>
        </body></html>"""
        return [html.encode('utf-8')]
