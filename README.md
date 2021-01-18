# queries

Hosts reusable log queries which are built into a single queries.json file.

## Query database structure

Queries are defined using the data model from src/model.py which builds
a JSON Validation schema, making easy to validate the file.

One example of file can be seen at [queries-example.yml](https://github.com/rdo-infra/queries/blob/main/src/data/queries-example.yml)

Both [elastic-search](https://www.elastic.co/guide/en/elasticsearch/reference/current/term-level-queries.html) and [artcl](https://opendev.org/openstack/ansible-role-collect-logs) can make use of `regex` searches.

Pattern is supposed to be an exact string match and if multiple are present
we could easily convert them into a regex or logstash expression that uses
logical `AND`.

### Pattern

On elastic-rechheck queries we have cases with multiple entries used on
patterns, like `message:foo AND message:bar`. This is why we also allow
a list of strings.

### Categories

A query can have only one category out of a determined list of possible
values, currently `infra` and `code` are allowed. These can be used to
list found matches in section, making them easier to read.

### Tags

Tags are also used to build the logstash queries. List of known values
already used inside elastic-recheck queries:

```yaml
tags:
  - console
  - console.html
  - devstack-gate-setup-host.txt
  - grenade.sh.txt
  - job-output.txt
  - screen-c-api.txt
  - screen-c-bak.txt
  - screen-n-cpu.txt
  - screen-n-sch.txt
  - screen-q-agt.txt
  - syslog.txt
```

When logstash query is build `OR` is used between multiple tags.

### Uncovered cases:

We do not currently support the exclusions like below (2/93 found):
```yaml
query: >-
  message:"RESULT_TIMED_OUT: [untrusted : git.openstack.org/openstack/tempest/playbooks/devstack-tempest.yaml@master]" AND
  tags:"console" AND NOT
  (build_name:"tempest-all" OR
   build_name:"tempest-slow" OR
   build_name:"tempest-slow-py3")

query2: >-
  (message: "FAILED with status: 137" OR
  message: "FAILED with status: 143" OR
  message: "RUN END RESULT_TIMED_OUT") AND
  NOT message:"POST-RUN END RESULT_TIMED_OUT" AND
  tags: "console"
```

To allow us to cover for corner cases not covered byt the generic format,
we could have an optional `logstash` key that mentions the query. When this
would be present, we woudl avoid building the logstash query ourselves and
just use it.

## Disable queries per backend

To avoid using a particular query on a particular backend we can make use of
``skip: ['er', 'artcl']``.
