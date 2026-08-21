---
title: "Traefik OCSP Documentation"
description: "Learn how to configure Traefik to use OCSP. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Install Configuration / TLS / OCSP"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/install-configuration/tls/ocsp.md"
source_url: "https://github.com/traefik/traefik/blob/b78307590625ada3e430d358b7947f11a0aef226/docs/content/reference/install-configuration/tls/ocsp.md"
---

# OCSP

Check certificate status and perform OCSP stapling.

## Overview

### OCSP Stapling

When OCSP is enabled, Traefik checks the status of every certificate in the store that provides an OCSP responder URL,
including the default certificate, and staples the OCSP response to the TLS handshake.
The OCSP check is performed when the certificate is loaded,
and once every hour until it is successful at the halfway point before the update date.

### Caching

Traefik caches the OCSP response as long as the associated certificate is provided by the configuration.
When a certificate is no longer provided,
the OCSP response has a 24 hour TTL waiting to be provided again or eventually removed.
The OCSP response is cached in memory and is not persisted between Traefik restarts.

## Configuration

### General

Enabling OCSP is part of the [install configuration](../boot-environment.md).
It can be defined by using a file (YAML or TOML) or CLI arguments:

**File (YAML)**

```yaml
## Static configuration
ocsp: {}
```

**File (TOML)**

```toml
## Static configuration
[ocsp]
```

**CLI**

```bash
## Static configuration
--ocsp=true
```

### Responder Overrides

The `responderOverrides` option defines the OCSP responder URLs to use instead of the one provided by the certificate.
This is useful when you want to use a different OCSP responder.

**File (YAML)**

```yaml
## Static configuration
ocsp:
  responderOverrides:
    foo: bar
```

**File (TOML)**

```toml
## Static configuration
[ocsp]
  [ocsp.responderOverrides]
    foo = "bar"
```

**CLI**

```bash
## Static configuration
--ocsp.responderoverrides.foo=bar
```
