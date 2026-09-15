import json, subprocess, sys

prev_raw = subprocess.check_output(['git', 'show', 'HEAD:notegraph.json'])
prev = json.loads(prev_raw)
cur = json.load(open('notegraph.json'))

ps = prev.get('stats', {})
cs = cur.get('stats', {})
print('previous stats:', ps)
print('current  stats:', cs)

node_delta = cs.get('nodes', 0) - ps.get('nodes', 0)
edge_delta = cs.get('edges', 0) - ps.get('edges', 0)
orphan_delta = cs.get('orphans', 0) - ps.get('orphans', 0)
bundled_delta = cs.get('bundled', 0) - ps.get('bundled', 0)

print('node_delta=' + str(node_delta))
print('edge_delta=' + str(edge_delta))
print('orphan_delta=' + str(orphan_delta))
print('bundled_delta=' + str(bundled_delta))

def compute_orphans(g):
    nodes = g.get('nodes', [])
    edges = g.get('edges', [])
    ind, outd = {}, {}
    for n in nodes:
        nid = n.get('id')
        ind[nid] = 0
        outd[nid] = 0
    for e in edges:
        s = e.get('source') or e.get('from')
        t = e.get('target') or e.get('to')
        if s in outd:
            outd[s] += 1
        if t in ind:
            ind[t] += 1
    return set(nid for nid in ind if ind[nid] == 0 and outd[nid] == 0)

def compute_bundled(g):
    return set(n.get('id') for n in g.get('nodes', []) if n.get('bundled'))

po = compute_orphans(prev)
co = compute_orphans(cur)
new_orphans = sorted(co - po)
resolved_orphans = sorted(po - co)

pb = compute_bundled(prev)
cb = compute_bundled(cur)
new_bundled = sorted(cb - pb)
resolved_bundled = sorted(pb - cb)

print('new_orphans(' + str(len(new_orphans)) + '):', new_orphans[:10])
print('resolved_orphans(' + str(len(resolved_orphans)) + '):', resolved_orphans[:10])
print('new_bundled(' + str(len(new_bundled)) + '):', new_bundled[:10])
print('resolved_bundled(' + str(len(resolved_bundled)) + '):', resolved_bundled[:10])

if new_bundled:
    verdict = str(len(new_bundled)) + ' new bundled note(s): ' + new_bundled[0] + '...'
elif new_orphans:
    verdict = str(len(new_orphans)) + ' new orphan(s): ' + new_orphans[0] + '...'
elif node_delta > 0 and orphan_delta <= 0 and bundled_delta <= 0:
    verdict = '+' + str(node_delta) + ' notes wired in'
elif edge_delta > 10:
    verdict = '+' + str(edge_delta) + ' new edges'
else:
    verdict = 'graph refreshed (' + str(cs.get('nodes',0)) + 'n / ' + str(cs.get('edges',0)) + 'e / ' + str(cs.get('bundled',0)) + 'b)'

print('VERDICT=' + verdict)
