---
title: "Traefik StripPrefixRegex Documentation"
description: "In Traefik Proxy's HTTP middleware, StripPrefixRegex removes prefixes from paths before forwarding requests, using regex. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / StripPrefixRegex"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/stripprefixregex.md"
source_url: "https://github.com/traefik/traefik/blob/2a2349356c01b1b1f7ecddb0c17b30c97f5241e7/docs/content/reference/routing-configuration/http/middlewares/stripprefixregex.md"
---

The `stripPrefixRegex` middleware strips the matching path prefix and stores it in an `X-Forwarded-Prefix` header.

> **Tip**
>
> Use a `stripPrefixRegex` middleware if your backend listens on the root path (`/`) but should be exposed on a specific prefix.

## Configuration Example

**Structured (YAML)**

```yaml
http:
  middlewares:
    test-stripprefixregex:
      stripPrefixRegex:
        regex:
          - "/foo/[a-z0-9]+/[0-9]+/"
```

**Structured (TOML)**

```toml
[http.middlewares]
  [http.middlewares.test-stripprefixregex.stripPrefixRegex]
    regex = ["/foo/[a-z0-9]+/[0-9]+/"]
```

**Labels**

```yaml
labels:
  - "traefik.http.middlewares.test-stripprefixregex.stripprefixregex.regex=/foo/[a-z0-9]+/[0-9]+/"
```

**Tags**

```yaml
{
  //..
  "Tags" : [
    "traefik.http.middlewares.test-stripprefixregex.stripprefixregex.regex=/foo/[a-z0-9]+/[0-9]+/"
  ]
}
- 
```

**Kubernetes**

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: test-stripprefixregex
spec:
  stripPrefixRegex:
    regex:
      - "/foo/[a-z0-9]+/[0-9]+/"
```

## Configuration Options

| Field                        | Description                                                                                                                                                                                                | Default | Required |
|:-----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|:---------|
| <a id="opt-regex" href="#opt-regex" title="#opt-regex">`regex`</a> | List of regular expressions to match the path prefix from the request URL.<br /> For instance, `/products` also matches `/products/shoes` and `/products/shirts`.<br />More information [here](#regex). | | No |

### regex

If your backend is serving assets (for example, images or JavaScript files), it can use the `X-Forwarded-Prefix` header to construct relative URLs.
Using the previous example, the backend should return `/products/shoes/image.png` (and not `/images.png`, which Traefik would likely not be able to associate with the same backend).

> **Tip**
>
> Regular expressions and replacements can be tested using online tools such as [Go Playground](https://play.golang.org/p/mWU9p-wk2ru) or the [Regex101](https://regex101.com/r/58sIgx/2).
>
> When defining a regular expression within YAML, any escaped character needs to be escaped twice: `example\.com` needs to be written as `example\\.com`.
