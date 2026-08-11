---
title: "Traefik InFlightConn Middleware - TCP"
description: "Limiting the number of simultaneous connections."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / TCP / Middlewares / InFlightConn"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/tcp/middlewares/inflightconn.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/reference/routing-configuration/tcp/middlewares/inflightconn.md"
---

To proactively prevent Services from being overwhelmed with high load, the number of allowed simultaneous connections by IP can be limited with the `inFlightConn` TCP middleware.

## Configuration Examples

**Structured (YAML)**

```yaml
# Limiting to 10 simultaneous connections
tcp:
  middlewares:
    test-inflightconn:
      inFlightConn:
        amount: 10
```

**Structured (TOML)**

```toml
# Limiting to 10 simultaneous connections
[tcp.middlewares]
  [tcp.middlewares.test-inflightconn.inFlightConn]
    amount = 10
```

**Labels**

```yaml
labels:
  - "traefik.tcp.middlewares.test-inflightconn.inflightconn.amount=10"
```

**Tags**

```json
// Limiting to 10 simultaneous connections
{
  //..
  "Tags" : [
    "traefik.tcp.middlewares.test-inflightconn.inflightconn.amount=10"
  ]
}
```

**Kubernetes**

```yaml
apiVersion: traefik.io/v1alpha1
kind: MiddlewareTCP
metadata:
  name: test-inflightconn
spec:
  inFlightConn:
    amount: 10
```

## Configuration Options

| Field | Description | Default | Required |
|:------|:------------|------------------|-------|
| <a id="opt-amount" href="#opt-amount" title="#opt-amount">`amount`</a> | The `amount` option defines the maximum amount of allowed simultaneous connections. <br /> The middleware closes the connection if there are already `amount` connections opened. | 0 | Yes |
