---
title: "Providing Dynamic Configuration to Traefik"
description: "Learn about the different methods for providing dynamic configuration to Traefik. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / Configuration Methods"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/dynamic-configuration-methods.md"
source_url: "https://github.com/traefik/traefik/blob/b78307590625ada3e430d358b7947f11a0aef226/docs/content/reference/routing-configuration/dynamic-configuration-methods.md"
---

# Providing Dynamic (Routing) Configuration to Traefik

Dynamic configuration—now also known as routing configuration—defines how Traefik routes incoming requests to the correct services. This is distinct from install configuration (formerly known as static configuration), which sets up Traefik’s core components and providers.

Depending on your environment and preferences, there are several ways to supply this routing configuration:

- File or Structured Provider: Use TOML or YAML files.
- Docker and ECS Providers: Use container labels.
- Kubernetes Providers: Use annotations.
- KV Providers : Use key-value pairs.
- Other Providers (Consul, Nomad, etc.) : Use tags.

## Using the File Provider

The File provider allows you to define routing configuration in static files using either TOML or YAML syntax. This method is ideal for environments where services cannot be automatically discovered or when you prefer to manage configurations manually.

### Enabling the File Provider

To enable the File provider, add the following to your Traefik install configuration:

**YAML**

```yaml
providers:
  file:
    directory: "/path/to/dynamic/conf"
```

**TOML**

```toml
[providers.file]
  directory = "/path/to/dynamic/conf"
```

> **Example — Example using the file provider to declare routers & services**
>
>   **File (YAML)**
>
>   ```yaml
>   http:
>     routers:
>       my-router:
>         rule: "Host(`example.com`)"
>         service: my-service
>
>     services:
>       my-service:
>         loadBalancer:
>           servers:
>             - url: "http://localhost:8080"
>   ```
>
>   **File (TOML)**
>
>   ```toml
>   [http]
>     [http.routers]
>       [http.routers.my-router]
>         rule = "Host(`example.com`)"
>         service = "my-service"
>
>     [http.services]
>       [http.services.my-service.loadBalancer]
>         [[http.services.my-service.loadBalancer.servers]]
>           url = "http://localhost:8080"
>   ```

## Using Labels With Docker and ECS

When using Docker or Amazon ECS, you can define routing configuration using container labels. This method allows Traefik to automatically discover services and apply configurations without the need for additional files.

> **Example — Example with Docker**
>
> When deploying a Docker container, you can specify labels to define routing rules and services:
>
> ```yaml
> services:
>   my-service:
>     image: my-image
>     labels:
>       - "traefik.http.routers.my-router.rule=Host(`example.com`)"
>       - "traefik.http.services.my-service.loadbalancer.server.port=80"
> ```

> **Example — Example with ECS**
>
> In ECS, you can use task definition labels to achieve the same effect:
>
> ```yaml
> {
>   "containerDefinitions": [
>     {
>       "name": "my-service",
>       "image": "my-image",
>       "dockerLabels": {
>         "traefik.http.routers.my-router.rule": "Host(`example.com`)",
>         "traefik.http.services.my-service.loadbalancer.server.port": "80"
>       }
>     }
>   ]
> }
> ```

## Using Kubernetes Providers

For Kubernetes providers, you can configure Traefik using the native Ingress or custom resources (like IngressRoute). Annotations in your Ingress or IngressRoute definition allow you to define routing rules and middleware settings. For example:

> **Example — Example with Kubernetes**
>
> ```yaml
> apiVersion: networking.k8s.io/v1
> kind: Ingress
> metadata:
>   name: whoami
>   namespace: apps
>   annotations:
>     traefik.ingress.kubernetes.io/router.entrypoints: websecure
>     traefik.ingress.kubernetes.io/router.priority: "42"
>     traefik.ingress.kubernetes.io/router.tls: "true"
>     traefik.ingress.kubernetes.io/router.tls.options: apps-opt@kubernetescrd
> spec:
>   rules:
>     - host: my-domain.example.com
>       http:
>         paths:
>           - path: /
>             pathType: Prefix
>             backend:
>               service:
>                 name: whoami
>                 port:
>                   number: 80
>   tls:
>     - secretName: supersecret
> ```

## Using Key-Value Pairs With KV Providers

For [KV providers](./other-providers/kv.md) you can configure Traefik with key-value pairs.

> **Example — Examples**
>
> **etcd**
>
> ```bash
> # Set a router rule
> etcdctl put /traefik/http/routers/my-router/rule "Host(`example.com`)"
> # Define the service associated with the router
> etcdctl put /traefik/http/routers/my-router/service "my-service"
> # Set the backend server URL for the service
> etcdctl put /traefik/http/services/my-service/loadbalancer/servers/0/url "http://localhost:8080"
> ```
>
> **Redis**
>
> ```bash
> # Set a router rule
> redis-cli set traefik/http/routers/my-router/rule "Host(`example.com`)"
> # Define the service associated with the router
> redis-cli set traefik/http/routers/my-router/service "my-service"
> # Set the backend server URL for the service
> redis-cli set traefik/http/services/my-service/loadbalancer/servers/0/url "http://localhost:8080"
> ```
>
> **ZooKeeper**
>
> ```bash
> # Set a router rule
> create /traefik/http/routers/my-router/rule "Host(`example.com`)"
> # Define the service associated with the router
> create /traefik/http/routers/my-router/service "my-service"
> # Set the backend server URL for the service
> create /traefik/http/services/my-service/loadbalancer/servers/0/url "http://localhost:8080"
> ```

## Using Tags With Other Providers

For providers that do not support labels, such as Consul & Nomad, you can use tags to provide routing configuration.

> **Example — Example**
>
> **Consul / Nomad**
>
> ```json
> {
>   "Name": "my-service",
>   "Tags": [
>     "traefik.http.routers.my-router.rule=Host(`example.com`)",
>     "traefik.http.services.my-service.loadbalancer.server.port=80"
>   ],
>   "Address": "localhost",
>   "Port": 8080
> }
> ```
