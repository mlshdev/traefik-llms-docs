---
title: "Traefik ReplacePath Documentation"
description: "In Traefik Proxy's HTTP middleware, ReplacePath updates paths before forwarding requests. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / ReplacePath"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/replacepath.md"
source_url: "https://github.com/traefik/traefik/blob/2a2349356c01b1b1f7ecddb0c17b30c97f5241e7/docs/content/reference/routing-configuration/http/middlewares/replacepath.md"
---

The `replacePath` middleware will:

- Replace the actual path with the specified one.
- Store the original path in a `X-Replaced-Path` header

## Configuration Examples

**Structured (YAML)**

```yaml
# Replace the path with /foo
http:
  middlewares:
    test-replacepath:
      replacePath:
        path: "/foo"
```

**Structured (TOML)**

```toml
# Replace the path with /foo
[http.middlewares]
  [http.middlewares.test-replacepath.replacePath]
    path = "/foo"
```

**Labels**

```yaml
# Replace the path with /foo
labels:
  - "traefik.http.middlewares.test-replacepath.replacepath.path=/foo"
```

**Tags**

```json
// Replace the path with /foo
{
  // ...
  "Tags" : [
    "traefik.http.middlewares.test-replacepath.replacepath.path=/foo"
  ]
} 
```

**Kubernetes**

```yaml
# Replace the path with /foo
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: test-replacepath
spec:
  replacePath:
    path: "/foo"
```

## Configuration Options

| Field | Description |
|:------|:------------|
| <a id="opt-path" href="#opt-path" title="#opt-path">`path`</a> | The `path` option defines the path to use as replacement in the request URL. |
