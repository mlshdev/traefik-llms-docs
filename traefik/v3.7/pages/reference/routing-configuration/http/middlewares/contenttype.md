---
title: "Traefik ContentType Documentation"
description: "Traefik Proxy's HTTP middleware automatically sets the `Content-Type` header value when it is not set by the backend. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / ContentType"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/contenttype.md"
source_url: "https://github.com/traefik/traefik/blob/0258b3a756f9c31659bc3745e7b160bd92a46af2/docs/content/reference/routing-configuration/http/middlewares/contenttype.md"
---

The `contentType` middleware sets the `Content-Type` header value to the media type detected from the response content,
when it is not set by the backend.

> **Info**
>
> The `contentType` middleware only applies when Traefik detects the MIME type. If any middleware (such as Headers or Compress) sets the `contentType` header at any point in the chain, the `contentType` middleware has no effect.

## Configuration Examples

**Structured (YAML)**

```yaml
# Enable auto-detection
http:
  middlewares:
    autodetect:
      contentType: {}
```

**Structured (TOML)**

```toml
# Enable auto-detection
[http.middlewares]
  [http.middlewares.autodetect.contentType]
```

**Labels**

```yaml
# Enable auto-detection
labels:
  - "traefik.http.middlewares.autodetect.contenttype=true"
```

**Tags**

```json
// Enable auto-detection
{
  // ...
  "Tags": [
    "traefik.http.middlewares.autodetect.contenttype=true"
  ]
}
```

**Kubernetes**

```yaml
# Enable auto-detection
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: autodetect
spec:
  contentType: {}
```
