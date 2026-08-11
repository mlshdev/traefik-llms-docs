---
title: "Traefik RedirectScheme Documentation"
description: "In Traefik Proxy's HTTP middleware, RedirectScheme redirects clients to different schemes/ports. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / RedirectScheme"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/redirectscheme.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/reference/routing-configuration/http/middlewares/redirectscheme.md"
---

The `RedirectScheme` middleware redirects the request if the request scheme is different from the configured scheme.

> **Warning — When behind another reverse-proxy**
>
> When there is at least one other reverse-proxy between the client and Traefik,
> the other reverse-proxy (i.e. the last hop) needs to be a [trusted](../../../install-configuration/entrypoints.md#configuration-options) one.
>
> Otherwise, Traefik would clean up the `X-Forwarded` headers coming from this last hop,
> and as the RedirectScheme middleware relies on them to determine the scheme used,
> it would not function as intended.

## Configuration Examples

**Structured (YAML)**

```yaml
# Redirect to https
http:
  middlewares:
    test-redirectscheme:
      redirectScheme:
        scheme: https
        permanent: true
```

**Structured (TOML)**

```toml
# Redirect to https
[http.middlewares]
  [http.middlewares.test-redirectscheme.redirectScheme]
    scheme = "https"
    permanent = true
```

**Labels**

```yaml
# Redirect to https
labels:
  - "traefik.http.middlewares.test-redirectscheme.redirectscheme.scheme=https"
  - "traefik.http.middlewares.test-redirectscheme.redirectscheme.permanent=true"
```

**Tags**

```json
// Redirect to https
{
  // ...
  "Tags": [
    "traefik.http.middlewares.test-redirectscheme.redirectscheme.scheme=https",
    "traefik.http.middlewares.test-redirectscheme.redirectscheme.permanent=true"
  ]
}

```

**Kubernetes**

```yaml
# Redirect to https
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: test-redirectscheme
spec:
  redirectScheme:
    scheme: https
    permanent: true
```

## Configuration Options

| Field                        | Description                                             | Default | Required |
|:-----------------------------|----------------------------------------------------------|:--------|:---------|
| <a id="opt-scheme" href="#opt-scheme" title="#opt-scheme">`scheme`</a> | Scheme of the new URL. | "" | Yes |
| <a id="opt-permanent" href="#opt-permanent" title="#opt-permanent">`permanent`</a> | Enable a permanent redirection. | false | No |
| <a id="opt-port" href="#opt-port" title="#opt-port">`port`</a> | Port of the new URL.<br />Set a string, **not** a numeric value. | "" | No |
