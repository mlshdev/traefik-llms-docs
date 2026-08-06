---
title: "Traefik AddPrefix Documentation"
description: "Learn how to implement the HTTP AddPrefix middleware in Traefik Proxy to updates request paths before being forwarded. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / AddPrefix"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/addprefix.md"
source_url: "https://github.com/traefik/traefik/blob/ead8b92dba6eca8c19e40287f986dc54a57325f4/docs/content/reference/routing-configuration/http/middlewares/addprefix.md"
---

The `addPrefix` middleware updates the path of a request before forwarding it.

## Configuration Examples

**Structured (YAML)**

```yaml
# Prefixing with /foo
http:
  middlewares:
    add-foo:
      addPrefix:
        prefix: "/foo"
```

**Structured (TOML)**

```toml
# Prefixing with /foo
[http.middlewares]
  [http.middlewares.add-foo.addPrefix]
    prefix = "/foo"
```

**Labels**

```yaml
# Prefixing with /foo
labels:
  - "traefik.http.middlewares.add-foo.addprefix.prefix=/foo"
```

**Tags**

```json
// Prefixing with /foo
{
  // ...
  "Tags": [
    "traefik.http.middlewares.add-foo.addprefix.prefix=/foo"
  ]
}
```

**Kubernetes**

```yaml
# Prefixing with /foo
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: add-foo
spec:
  addPrefix:
    prefix: /foo
```

## Configuration Options

| Field  | Description                                                                                                                                                                                                | Default | Required |
|:-----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|:---------|
| <a id="opt-prefix" href="#opt-prefix" title="#opt-prefix">`prefix`</a> | String to add **before** the current path in the requested URL. It should include a leading slash (`/`). | "" | Yes |
