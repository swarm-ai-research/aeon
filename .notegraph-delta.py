import json, subprocess
cur = json.load(open('notegraph.json'))
head = json.loads(subprocess.check_output(['git', 'show', 'HEAD:notegraph.json']))

def orph(g):
    return set(n['id'] for n in g['nodes'] if n.get('inDegree',0)==0 and n.get('outDegree',0)==0)

def bund(g):
    return set(n['id'] for n in g['nodes'] if n.get('bundled'))

def ids(g):
    return set(n['id'] for n in g['nodes'])

cur_ids, head_ids = ids(cur), ids(head)
cur_orph, head_orph = orph(cur), orph(head)
cur_bund, head_bund = bund(cur), bund(head)

new_nodes = sorted(cur_ids - head_ids)
removed_nodes = sorted(head_ids - cur_ids)
new_orphans = sorted(cur_orph - head_orph)
resolved_orphans = sorted(head_orph - cur_orph)
new_bundled = sorted(cur_bund - head_bund)
resolved_bundled = sorted(head_bund - cur_bund)

print("new_nodes:", new_nodes)
print("removed_nodes:", removed_nodes)
print("new_orphans:", new_orphans)
print("resolved_orphans:", resolved_orphans)
print("new_bundled:", new_bundled)
print("resolved_bundled:", resolved_bundled)

s_c, s_h = cur['stats'], head['stats']
print("node_delta:", s_c['nodes'] - s_h['nodes'])
print("edge_delta:", s_c['edges'] - s_h['edges'])
print("hard_delta:", s_c['hard'] - s_h['hard'])
print("soft_delta:", s_c['soft'] - s_h['soft'])
print("orphan_delta:", s_c['orphans'] - s_h['orphans'])
print("bundled_delta:", s_c['bundled'] - s_h['bundled'])
print("atomic_delta:", s_c['atomic'] - s_h['atomic'])
