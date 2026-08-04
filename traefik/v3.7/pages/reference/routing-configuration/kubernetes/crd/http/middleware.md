---
title: "Traefik Kubernetes Middleware Documentation"
description: "Learn how to configure a Traefik Proxy Kubernetes Middleware to reach Services, which handle incoming requests. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Kubernetes / Kubernetes CRD / HTTP / Middleware"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/kubernetes/crd/http/middleware.md"
source_url: "https://github.com/traefik/traefik/blob/0258b3a756f9c31659bc3745e7b160bd92a46af2/docs/content/reference/routing-configuration/kubernetes/crd/http/middleware.md"
---

`Middleware` is the CRD implementation of a [Traefik middleware](../../../http/middlewares/overview.md).

Before creating `Middleware` objects, you need to apply the [Traefik Kubernetes CRDs](https://doc.traefik.io/traefik/reference/dynamic-configuration/kubernetes-crd/#definitions) to your Kubernetes cluster.

This registers the `Middleware` kind and other Traefik-specific resources.

> **Tip — Cross-provider namespace**
>
> As Kubernetes also has its own notion of namespace, one should not confuse the Kubernetes namespace of a resource (in the reference to the middleware) with the [provider namespace](../../../../install-configuration/providers/overview.md#provider-namespace), when the definition of the middleware comes from another provider. In this context, specifying a namespace when referring to the resource does not make any sense, and will be ignored. Additionally, when you want to reference a Middleware from the CRD Provider, you have to append the namespace of the resource in the resource-name as Traefik appends the namespace internally automatically.

> **Note — Cross-Namespace References**
>
> In the example below, the middleware is defined in the `foo` namespace while being referenced from an IngressRoute in another namespace. To enable such cross-namespace references, the `allowCrossNamespace` option must be enabled in the Traefik [Kubernetes CRD provider](../../../../install-configuration/providers/kubernetes/kubernetes-crd.md#configuration-options) configuration. If you prefer to avoid this requirement, you can define and reference the Middleware within the same namespace.

## Configuration Example

**Middleware**

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: stripprefix
  namespace: foo

spec:
  stripPrefix:
    prefixes:
      - /stripit
```

**IngressRoute**

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: ingressroutebar

spec:
  entryPoints:
    - web
  routes:
  - match: Host(`example.com`) && PathPrefix(`/stripit`)
    kind: Rule
    services:
    - name: whoami
      port: 80
    middlewares:
    - name: stripprefix
      namespace: foo
```

For more information about the available middlewares, navigate to the dedicated [middlewares overview section](../../../http/middlewares/overview.md).
