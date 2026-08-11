---
title: "Traefik TCP Middlewares IPAllowList"
description: "Learn how to use IPAllowList in TCP middleware for limiting clients to specific IPs in Traefik Proxy. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / TCP / Middlewares / IPAllowList"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/tcp/middlewares/ipallowlist.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/reference/routing-configuration/tcp/middlewares/ipallowlist.md"
---

`iPAllowList` limits allowed requests based on the client IP.

## Configuration Examples

**Structured (YAML)**

```yaml
# Accepts request from defined IP
tcp:
  middlewares:
    test-ipallowlist:
      ipAllowList:
        sourceRange:
          - "127.0.0.1/32"
          - "192.168.1.7"
```

**Structured (TOML)**

```toml
# Accepts request from defined IP
[tcp.middlewares]
  [tcp.middlewares.test-ipallowlist.ipAllowList]
    sourceRange = ["127.0.0.1/32", "192.168.1.7"]
```

**Labels**

```yaml
# Accepts connections from defined IP
labels:
  - "traefik.tcp.middlewares.test-ipallowlist.ipallowlist.sourcerange=127.0.0.1/32, 192.168.1.7"
```

**Tags**

```json
// Accepts request from defined IP
{
  //...
  "Tags" : [
    "traefik.tcp.middlewares.test-ipallowlist.ipallowlist.sourcerange=127.0.0.1/32, 192.168.1.7"
  ]
}
```

**Kubernetes**

```yaml
apiVersion: traefik.io/v1alpha1
kind: MiddlewareTCP
metadata:
  name: test-ipallowlist
spec:
  ipAllowList:
    sourceRange:
      - 127.0.0.1/32
      - 192.168.1.7
```

## Configuration Options

| Field | Description | Default | Required |
|:------|:------------|------------------|-------|
| <a id="opt-sourceRange" href="#opt-sourceRange" title="#opt-sourceRange">`sourceRange`</a> | The `sourceRange` option sets the allowed IPs (or ranges of allowed IPs by using CIDR notation).| | Yes |
