import os, sqlite3, json, html
from flask import Flask, request, redirect, abort, render_template_string, Response
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
def database_path():
    if os.getenv('VERCEL') == '1':
        return '/tmp/training.sqlite3'
    return os.getenv('TRAINING_DB') or 'training.sqlite3'
DB = database_path()
def db():
    c = sqlite3.connect(DB)
    c.execute('CREATE TABLE IF NOT EXISTS revisions (id INTEGER PRIMARY KEY, title TEXT NOT NULL, steps TEXT NOT NULL, approved INTEGER NOT NULL DEFAULT 0)')
    return c
PAGE = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Training Studio</title><style>body{font:18px system-ui;max-width:850px;margin:3rem auto;padding:1rem;background:#f6f4ed;color:#173d35}textarea,input{width:100%;font:inherit}button{padding:.7rem}article{border-top:1px solid;padding:1rem 0}</style><h1>Training Studio</h1>{% if demo %}<p role="alert"><strong>Temporary public demo:</strong> use fictional data only. Records are shared and may disappear at any time.</p>{% endif %}<p>Draft, approve, and export a consistent procedure.</p><form method="post" action="/draft"><label>Procedure title<input name="title" required maxlength="120"></label><label>Steps (one per line; include source timestamps)<textarea name="steps" rows="8" required></textarea></label><button>Save new revision</button></form>{% for id,title,steps,approved in rows %}<article><h2>{{title}} · Revision {{id}}</h2><ol>{% for step in steps %}<li>{{step}}</li>{% endfor %}</ol>{% if approved %}<a href="/export/{{id}}/checklist">Checklist</a> · <a href="/export/{{id}}/diagram">Mermaid source</a>{% else %}<form method="post" action="/approve/{{id}}"><button>Approve this revision</button></form>{% endif %}</article>{% endfor %}</html>"""
@app.get('/')
def index():
    with db() as c:
        rows = [(i,t,json.loads(s),a) for i,t,s,a in c.execute('SELECT * FROM revisions ORDER BY id DESC')]
    return render_template_string(PAGE, rows=rows, demo=os.getenv('VERCEL') == '1')
@app.post('/draft')
def draft():
    title = request.form.get('title','').strip()
    steps = [s.strip() for s in request.form.get('steps','').splitlines() if s.strip()]
    if not title or len(title)>120 or not 1<=len(steps)<=15 or any(len(s)>500 for s in steps): abort(400)
    with db() as c:
        c.execute('INSERT INTO revisions(title,steps) VALUES (?,?)',(title,json.dumps(steps)))
    return redirect('/')
@app.post('/approve/<int:i>')
def approve(i):
    with db() as c:
        if not c.execute('UPDATE revisions SET approved=1 WHERE id=?',(i,)).rowcount: abort(404)
    return redirect('/')
@app.get('/export/<int:i>/<kind>')
def export(i,kind):
    with db() as c:
        row=c.execute('SELECT title,steps FROM revisions WHERE id=? AND approved=1',(i,)).fetchone()
    if not row: abort(404)
    title, raw = row
    steps=json.loads(raw)
    if kind=='checklist':
        body=f'{title} — revision {i}\n'+'\n'.join('[ ] '+s for s in steps)
    elif kind=='diagram':
        # Mermaid entity escapes prevent labels from introducing syntax.
        def safe(s):
            return ''.join(ch if ch.isalnum() or ch in ' .,:/-' else f'#{ord(ch)};' for ch in s)
        body=f'%% Revision {i}\nflowchart TD\n'+'\n'.join(f'  S{n}["{safe(s)}"]' for n,s in enumerate(steps))+'\n'+'\n'.join(f'  S{n} --> S{n+1}' for n in range(len(steps)-1))
    else: abort(404)
    return Response(body,mimetype='text/plain',headers={'Content-Disposition':f'attachment; filename=revision-{i}-{kind}.txt'})
@app.get('/health')
def health():
    with db() as c: c.execute('SELECT 1')
    return {'status':'ok'}
