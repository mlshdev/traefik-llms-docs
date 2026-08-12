---
title: "Traefik ReplacePathRegex Documentation"
description: "In Traefik Proxy's HTTP middleware, ReplacePathRegex updates paths before forwarding requests, using a regex. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / ReplacePathRegex"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/replacepathregex.md"
source_url: "https://github.com/traefik/traefik/blob/21a4ca1fad46ceca9b7d7903eeaf3721325f3e50/docs/content/reference/routing-configuration/http/middlewares/replacepathregex.md"
---

The `replacePathRegex` middleware will:

- Replace the matching path with the specified one.
- Store the original path in an `X-Replaced-Path` header

## Configuration Examples

**File (YAML)**

```yaml
# Replace path with regex
http:
  middlewares:
    test-replacepathregex:
      replacePathRegex:
        regex: "^/foo/(.*)"
        replacement: "/bar/$1"
```

**File (TOML)**

```toml
# Replace path with regex
[http.middlewares]
  [http.middlewares.test-replacepathregex.replacePathRegex]
    regex = "^/foo/(.*)"
    replacement = "/bar/$1"
```

**Kubernetes**

```yaml
# Replace path with regex
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: test-replacepathregex
spec:
  replacePathRegex:
    regex: "^/foo/(.*)"
    replacement: "/bar/$1"
```

**Docker & Swarm**

```yaml
# Replace path with regex
labels:
  - "traefik.http.middlewares.test-replacepathregex.replacepathregex.regex=^/foo/(.*)"
  - "traefik.http.middlewares.test-replacepathregex.replacepathregex.replacement=/bar/$$1"
```

**Consul Catalog**

```yaml
# Replace path with regex
- "traefik.http.middlewares.test-replacepathregex.replacepathregex.regex=^/foo/(.*)"
- "traefik.http.middlewares.test-replacepathregex.replacepathregex.replacement=/bar/$1"
```

## Configuration Options

| Field                        | Description      | Default | Required |
|:-----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|:---------|
| <a id="opt-regex" href="#opt-regex" title="#opt-regex">`regex`</a> | Regular expression to match and capture the path from the request URL. | | Yes |
| <a id="opt-replacement" href="#opt-replacement" title="#opt-replacement">`replacement`</a> | Replacement path format, which can include captured variables.<br /> `$1x` is equivalent to `${1x}`, not `${1}x` (see [Regexp.Expand](https://golang.org/pkg/regexp/#Regexp.Expand)), so use `${1}` syntax. | | No 

> **Tip**
>
> Regular expressions and replacements can be tested using online tools such as [Go Playground](https://play.golang.org/p/mWU9p-wk2ru) or the [Regex101](https://regex101.com/r/58sIgx/2).
>
> When defining a regular expression within YAML, any escaped character needs to be escaped twice: `example\.com` needs to be written as `example\\.com`.
