---
title: "Tracing"
description: "Tracing in Traefik Proxy allows you to track the flow of operations within your system. Using traces and spans, you can identify performance bottlenecks and pinpoint applications causing slowdowns to optimize response times effectively."
section: "Observe"
breadcrumb: "Observe / Tracing"
traefik_version: "v3.7"
upstream_path: "docs/content/observe/tracing.md"
source_url: "https://github.com/traefik/traefik/blob/21a4ca1fad46ceca9b7d7903eeaf3721325f3e50/docs/content/observe/tracing.md"
---

# Tracing

Tracing in Traefik Proxy allows you to track the flow of operations within your system. Using traces and spans, you can identify performance bottlenecks and pinpoint applications causing slowdowns to optimize response times effectively.

Traefik Proxy uses [OpenTelemetry](https://opentelemetry.io/) to export traces. OpenTelemetry is an open-source observability framework. You can send traces to an OpenTelemetry collector, which can then export them to a variety of backends like Jaeger, Zipkin, or Datadog.

## Configuration

To enable tracing in Traefik Proxy, you need to configure it in your static configuration file or Helm values if you are using the [Helm chart](https://github.com/traefik/traefik-helm-chart). The following example shows how to configure the OpenTelemetry provider to send traces to a collector via HTTP.

**Structured (YAML)**

```yaml
tracing:
  otlp:
    http:
      endpoint: http://myotlpcollector:4318/v1/traces
```

**Structured (TOML)**

```toml
[tracing.otlp.http]
  endpoint = "http://myotlpcollector:4318/v1/traces"
```

**Helm Chart Values**

```yaml
# values.yaml
tracing:
  otlp:
    enabled: true
    http:
      enabled: true
      endpoint: http://myotlpcollector:4318/v1/traces
```

> **Info**
>
> For detailed configuration options, refer to the [tracing reference documentation](../reference/install-configuration/observability/tracing.md).

## Per-Router Tracing

You can enable or disable tracing for a specific router. This is useful for turning off tracing for specific routes while keeping it on globally.

Here's an example of disabling tracing on a specific router:

**Structured (YAML)**

```yaml
http:
  routers:
    my-router:
      rule: "Host(`example.com`)"
      service: my-service
      observability:
        tracing: false
```

**Structured (TOML)**

```toml
[http.routers.my-router.observability]
  tracing = false
```

**Kubernetes**

```yaml
# ingressoute.yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: my-router
spec:
  routes:
    - kind: Rule
      match: Host(`example.com`)
      services:
        - name: my-service
          port: 80
      observability:
        tracing: false
```

**Labels**

```yaml
labels:
  - "traefik.http.routers.my-router.observability.tracing=false"
```

**Tags**

```json
{
  // ...
  "Tags": [
    "traefik.http.routers.my-router.observability.tracing=false"
  ]
}
```

When the `observability` options are not defined on a router, it inherits the behavior from the [entrypoint's observability configuration](./overview.md), or the global one.
