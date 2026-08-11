---
title: "Traefik UDP Services Documentation"
description: "A service is in charge of connecting incoming requests to the Servers that can handle them. Read the technical documentation. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / UDP / Service"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/udp/service.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/reference/routing-configuration/udp/service.md"
---

 

### General

Each of the fields of the service section represents a kind of service.
Which means, that for each specified service, one of the fields, and only one,
has to be enabled to define what kind of service is created.
Currently, the two available kinds are `LoadBalancer`, and `Weighted`.

## Servers Load Balancer

The servers load balancer is in charge of balancing the requests between the servers of the same service.

### Servers

The Servers field defines all the servers that are part of this load-balancing group,
i.e. each address (IP:Port) on which an instance of the service's program is deployed.

#### Configuration Example

A Service with One Server -- Using the [File Provider](../../install-configuration/providers/others/file.md)

**Structured (YAML)**

```yaml
## Dynamic configuration
udp:
  services:
    my-service:
      loadBalancer:
        servers:
          - address: "xx.xx.xx.xx:xx"
```

**Structured (TOML)**

```toml
## Dynamic configuration
[udp.services]
  [udp.services.my-service.loadBalancer]
    [[udp.services.my-service.loadBalancer.servers]]
      address = "xx.xx.xx.xx:xx"
```

## Weighted Round Robin

The Weighted Round Robin (alias `WRR`) load-balancer of services is in charge of balancing the connections between multiple services based on provided weights.

This strategy is only available to load balance between [services](./service.md) and not between servers.

> **Info — Supported Providers**
>
> This strategy can currently be defined with the [File provider](../../install-configuration/providers/others/file.md)
> and the [Kubernetes CRD provider (IngressRouteUDP)](../kubernetes/crd/udp/ingressrouteudp.md).

**Structured (YAML)**

```yaml
udp:
  services:
    app:
      weighted:
        services:
          - name: appv1
            weight: 3
          - name: appv2
            weight: 1

    appv1:
      loadBalancer:
        servers:
          - address: "xxx.xxx.xxx.xxx:8080"

    appv2:
      loadBalancer:
        servers:
          - address: "xxx.xxx.xxx.xxx:8080"
```

**Structured (TOML)**

```toml
[udp.services]
  [udp.services.app]
    [[udp.services.app.weighted.services]]
      name = "appv1"
      weight = 3
    [[udp.services.app.weighted.services]]
      name = "appv2"
      weight = 1

  [udp.services.appv1]
    [udp.services.appv1.loadBalancer]
      [[udp.services.appv1.loadBalancer.servers]]
        address = "xxx.xxx.xxx.xxx:8080"

  [udp.services.appv2]
    [udp.services.appv2.loadBalancer]
      [[udp.services.appv2.loadBalancer.servers]]
        address = "xxx.xxx.xxx.xxx:8080"
```

### Configuration Options

| Field | Description | Default | Required |
|-------|-------------|---------|----------|
| <a id="opt-services" href="#opt-services" title="#opt-services">`services`</a> | Defines the list of services to load balance between. | | Yes |
| <a id="opt-services-name" href="#opt-services-name" title="#opt-services-name">`services.name`</a> | The name of the service to load balance to. | "" | Yes |
| <a id="opt-services-weight" href="#opt-services-weight" title="#opt-services-weight">`services.weight`</a> | The weight applied to the service when balancing connections. | 1 | No |

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
