---
title: "Traefik FastProxy Experimental Configuration"
description: "This section of the Traefik Proxy documentation explains how to use the new FastProxy install configuration option."
section: "Reference"
breadcrumb: "Reference / Install Configuration / Experimental / FastProxy"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/install-configuration/experimental/fastproxy.md"
source_url: "https://github.com/traefik/traefik/blob/21a4ca1fad46ceca9b7d7903eeaf3721325f3e50/docs/content/reference/install-configuration/experimental/fastproxy.md"
---

# Traefik FastProxy Experimental Configuration

## Overview

This guide provides instructions on how to configure and use the new experimental `fastProxy` install configuration option in Traefik. The `fastProxy` option introduces a high-performance reverse proxy designed to enhance the performance of routing.

> **Info — Limitations**
>
> Please note that the new fast proxy implementation does not work with HTTP/2.
> This means that when a H2C or HTTPS request with [HTTP2 enabled](../../routing-configuration/http/load-balancing/serverstransport.md#opt-disableHTTP2) is sent to a backend, the fallback proxy is the regular one.
>
> Additionnaly, observability features like tracing and OTEL semconv metrics are not supported for the moment.

> **Warning — Experimental**
>
> The `fastProxy` option is currently experimental and subject to change in future releases.
> Use with caution in production environments.

## Enabling FastProxy

The fastProxy option is an install configuration parameter.
To enable it, you need to configure it in your Traefik install configuration

**File (YAML)**

```yaml
experimental:
  fastProxy: {}
```

**File (TOML)**

```toml
[experimental.fastProxy]
```

**CLI**

```bash
--experimental.fastProxy
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| <a id="opt-experimental-fastProxy-debug" href="#opt-experimental-fastProxy-debug" title="#opt-experimental-fastProxy-debug">`experimental.fastProxy.debug`</a> | `bool` | `false` | Enable debug mode for the FastProxy implementation. |
