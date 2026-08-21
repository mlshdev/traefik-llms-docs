---
title: "Metrics"
description: "Metrics in Traefik Proxy offer a comprehensive view of your infrastructure's health. They allow you to monitor critical indicators like incoming traffic volume. Metrics graphs and visualizations are helpful during incident triage in understanding the causes and implementing proactive measures."
section: "Observe"
breadcrumb: "Observe / Metrics"
traefik_version: "v3.7"
upstream_path: "docs/content/observe/metrics.md"
source_url: "https://github.com/traefik/traefik/blob/b78307590625ada3e430d358b7947f11a0aef226/docs/content/observe/metrics.md"
---

# Metrics

Metrics in Traefik Proxy offer a comprehensive view of your infrastructure's health. They allow you to monitor critical indicators like incoming traffic volume. Metrics graphs and visualizations are helpful during incident triage in understanding the causes and implementing proactive measures.

## Available Metrics Providers

Traefik Proxy supports the following metrics providers:

- OpenTelemetry
- Prometheus
- Datadog
- InfluxDB 2.X
- StatsD

## Configuration

To enable metrics in Traefik Proxy, you need to configure the metrics provider in your static configuration file or helm values if you are using the [Helm chart](https://github.com/traefik/traefik-helm-chart). The following example shows how to configure the OpenTelemetry provider to send metrics to a collector.

**Structured (YAML)**

```yaml
metrics:
  otlp:
    http:
      endpoint: http://myotlpcollector:4318/v1/metrics
```

**Structured (TOML)**

```toml
[metrics.otlp.http]
  endpoint = "http://myotlpcollector:4318/v1/metrics"
```

**Helm Chart Values**

```yaml
# values.yaml
metrics:
  # Disable Prometheus (enabled by default)
  prometheus: null
  # Enable providing OTel metrics
  otlp:
    enabled: true
    http:
      enabled: true
      endpoint: http://myotlpcollector:4318/v1/metrics
```

## Per-Router Metrics

You can enable or disable metrics collection for a specific router. This can be useful for excluding certain routes from your metrics data.

Here's an example of disabling metrics on a specific router:

**Structured (YAML)**

```yaml
http:
  routers:
    my-router:
      rule: "Host(`example.com`)"
      service: my-service
      observability:
        metrics: false
```

**Structured (TOML)**

```toml
[http.routers.my-router.observability]
  metrics = false
```

**Kubernetes**

```yaml
# ingressroute.yaml
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
        metrics: false
```

**Labels**

```bash
labels:
  - "traefik.http.routers.my-router.observability.metrics=false"
```

**Tags**

```json
{
  // ...
  "Tags": [
    "traefik.http.routers.my-router.observability.metrics=false"
  ]
}
```

When the `observability` options are not defined on a router, it inherits the behavior from the [entrypoint's observability configuration](./overview.md), or the global one.

> **Info**
>
> For detailed configuration options, refer to the [reference documentation](../reference/install-configuration/observability/metrics.md).
