import subprocess, os, time

now = int(time.time())

def git_ts(path):
    try:
        r = subprocess.run(['git', 'log', '-1', '--format=%ct', '--', path], capture_output=True, text=True)
        ts = r.stdout.strip()
        return int(ts) if ts else None
    except:
        return None

def stat_ts(path):
    try:
        return int(os.path.getmtime(path))
    except:
        return None

def age_hours(ts):
    if ts is None:
        return None
    return (now - ts) / 3600

print('=== .outputs ===')
out_dir = '.outputs'
if os.path.isdir(out_dir):
    for f in sorted(os.listdir(out_dir)):
        path = os.path.join(out_dir, f)
        if not os.path.isfile(path):
            continue
        ts = git_ts(path)
        src = 'git' if ts else 'stat'
        if ts is None:
            ts = stat_ts(path)
        h = age_hours(ts)
        print(f'{path}|{src}|{round(h,1) if h is not None else "NONE"}h')

print('=== memory/topics ===')
topics_dir = 'memory/topics'
if os.path.isdir(topics_dir):
    for f in sorted(os.listdir(topics_dir)):
        path = os.path.join(topics_dir, f)
        if not os.path.isfile(path):
            continue
        ts = git_ts(path)
        src = 'git' if ts else 'stat'
        if ts is None:
            ts = stat_ts(path)
        h = age_hours(ts)
        print(f'{path}|{src}|{round(h,1) if h is not None else "NONE"}h')

print('=== articles ===')
articles_dir = 'articles'
if os.path.isdir(articles_dir):
    for f in sorted(os.listdir(articles_dir)):
        path = os.path.join(articles_dir, f)
        if not os.path.isfile(path):
            continue
        ts = git_ts(path)
        src = 'git' if ts else 'stat'
        if ts is None:
            ts = stat_ts(path)
        h = age_hours(ts)
        print(f'{path}|{src}|{round(h,1) if h is not None else "NONE"}h')

print('=== memory/state ===')
state_dir = 'memory/state'
if os.path.isdir(state_dir):
    for f in sorted(os.listdir(state_dir))[:20]:
        path = os.path.join(state_dir, f)
        if not os.path.isfile(path):
            continue
        ts = git_ts(path)
        src = 'git' if ts else 'stat'
        if ts is None:
            ts = stat_ts(path)
        h = age_hours(ts)
        print(f'{path}|{src}|{round(h,1) if h is not None else "NONE"}h')

print(f'now={now}')
