# Permission matrix (Week 2)

| Action | Default permission | Approval needed | Allowed result |
|---|---:|---:|---|
| `read_email` | Allow | No | Read synthetic message only |
| `draft_email` | Allow | No | Create synthetic in-memory draft only |
| `send_email` | Deny | Approval cannot override deny | No send effect |
| Unknown action | Deny | N/A | No effect |

The executor validates the current permission at execution time, after the request is proposed. An agent request, a valid-looking approval, or an earlier permission state cannot override a current denial. Week 2's `send_email` default is explicitly forbidden, so even a matching approval cannot authorize it. Arguments must match the exact action schema and contain non-empty strings. The trace records `proposed`, then an `approved` or `denied` decision, and only records `executed` if an effect actually occurs.

This is a local simulation; “sent” is never performed against an external service. For the default policy, a send attempt is denied and the `sent` list remains empty.
