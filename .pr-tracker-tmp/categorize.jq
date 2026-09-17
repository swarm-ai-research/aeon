def daysBetween(a; b): ((b|fromdateiso8601) - (a|fromdateiso8601)) / 86400 | floor;
.data.search.nodes
| map(select(.headRefName != null))
| map(. + {
    _prefixMatch: (.headRefName | test("^(ai/|security/|fix/security/|aeon/|fix/|hook-submission/)")),
    _ageDays: daysBetween(.createdAt; $today),
    _daysSinceMerge: (if .mergedAt then daysBetween(.mergedAt; $today) else null end),
    _daysSinceClose: (if .closedAt and .mergedAt == null then daysBetween(.closedAt; $today) else null end),
    _lastReview: (.reviews.nodes[0].submittedAt // null),
    _authorEmail: (.commits.nodes[0].commit.author.email // "")
  })
| map(select(._prefixMatch))
