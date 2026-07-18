import subprocess, json, pathlib, sys

query = '''
{
  search(query: "author:aeonframework is:pr sort:updated-desc", type: ISSUE, first: 60) {
    nodes {
      ... on PullRequest {
        number
        title
        state
        headRefName
        url
        createdAt
        updatedAt
        mergedAt
        closedAt
        repository { nameWithOwner }
        reviews(last: 1) { nodes { state submittedAt } }
        comments { totalCount }
        commits(last: 1) { nodes { commit { author { email } } } }
      }
    }
  }
}
'''
r = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={query}'],
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.stderr.write(r.stderr)
    sys.exit(r.returncode)
pathlib.Path('.pr-tracker-tmp/raw.json').write_text(r.stdout)
data = json.loads(r.stdout)
nodes = data.get('data', {}).get('search', {}).get('nodes', [])
print(f'nodes: {len(nodes)}')
for n in nodes:
    email = ((n.get('commits') or {}).get('nodes') or [{}])[0].get('commit', {}).get('author', {}).get('email', '')
    print(f"  #{n['number']} {n['repository']['nameWithOwner']} state={n['state']} head={n['headRefName']} email={email} updated={n.get('updatedAt')}")
