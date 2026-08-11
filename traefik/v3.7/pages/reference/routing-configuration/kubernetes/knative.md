---
title: "Traefik Knative Documentation"
description: "The Knative provider can be used for routing and load balancing in Traefik Proxy. View examples in the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Kubernetes / Knative"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/kubernetes/knative.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/reference/routing-configuration/kubernetes/knative.md"
---

# Traefik & Knative

When using the Knative provider, Traefik leverages Knative's Custom Resource Definitions (CRDs) to obtain its routing configuration. 
For detailed information on Knative concepts and resources, refer to the official [documentation](https://knative.dev/docs/).

The Knative provider supports versions [v1.19.0](https://github.com/knative/serving/releases/tag/knative-v1.19.0) and [v1.20.0](https://github.com/knative/serving/releases/tag/knative-v1.20.0) of the specification.

## Deploying a Knative Service

A `Service` is a core resource in the Knative specification that defines the entry point for traffic into a Knative application. 
It is linked to a `Ingress`, which specifies the Knative networking controller responsible for managing and handling the traffic, 
ensuring that it is directed to the appropriate Knative backend services.

The following `Service` manifest configures the running Traefik controller to handle the incoming traffic.

```yaml
---
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: helloworld-go
  namespace: default
spec:
  template:
    spec:
      containers:
        - image: gcr.io/knative-samples/helloworld-go
          env:
            - name: TARGET
              value: "Go Sample v1"
```

Once everything is deployed, sending a `GET` request to the HTTP endpoint should return the following response:

```shell
$ curl http://helloworld-go.default.example.com

Hello Go Sample v1!
```

> **Note**
>
> The `example.com` domain is the public domain configured when deploying the Traefik controller.
> Check out [the install configuration](../../install-configuration/providers/kubernetes/knative.md) for more details.

### Tag based routing

To add tag-based routing with percentage in Knative, you can define the `traffic` section in your `Service` manifest to include different revisions with specific tags and percentages. 
Here is an example:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: helloworld-go
  namespace: default
spec:
  template:
    spec:
      containers:
        - image: gcr.io/knative-samples/helloworld-go
          env:
            - name: TARGET
              value: "Go Sample v2"
  traffic:
    - tag: v1
      revisionName: helloworld-go-00001
      percent: 50
    - tag: v2
      revisionName: helloworld-go-00002
      percent: 50
```

In this example:
- The `traffic` section specifies two revisions (`helloworld-go-00001` and `helloworld-go-00002`) with tags `v1` and `v2`, each receiving 50% of the traffic.
- The `tag` field allows you to route traffic to specific revisions using the tag.

You can access the tagged revisions using these URLs:

- `http://v1-helloworld-go.default.example.com`
- `http://v2-helloworld-go.default.example.com`

Use the default URL to access percentage-based routing:

- `http://helloworld-go.default.example.com`

### HTTP/HTTPS

Check out the Knative documentation for [HTTP/HTTPS configuration](https://knative.dev/docs/serving/encryption/external-domain-tls/#configure-external-domain-encryption).

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
