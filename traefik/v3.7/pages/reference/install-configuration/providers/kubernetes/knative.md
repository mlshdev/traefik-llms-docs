---
title: "Traefik Knative Documentation"
description: "Learn how to use the Knative as a provider for configuration discovery in Traefik Proxy. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Install Configuration / Configuration Discovery / Kubernetes / Knative"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/install-configuration/providers/kubernetes/knative.md"
source_url: "https://github.com/traefik/traefik/blob/473e27980fe40f447ada70783ae28aabae86107d/docs/content/reference/install-configuration/providers/kubernetes/knative.md"
---

# Traefik & Knative

The Traefik Knative provider integrates with Knative Serving to provide advanced traffic management and routing capabilities for serverless applications.

[Knative](https://knative.dev) is a Kubernetes-based platform that enables serverless workloads with features like scale-to-zero, 
automatic scaling, and revision management.

The provider watches Knative `Ingress` resources and automatically configures Traefik routing rules,
enabling seamless integration between Traefik's networking capabilities and Knative's serverless platform.

## Requirements

Traefik follows the [Kubernetes support policy](https://kubernetes.io/releases/version-skew-policy/#supported-versions),
and supports at least the latest three minor versions of Kubernetes.
General functionality cannot be guaranteed for older versions.

1. Install/update the Knative CRDs.

    ```bash
    kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.0/serving-crds.yaml
    ```

2. Install the Knative Serving core components.

    ```bash
    kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.0/serving-core.yaml
    ```

3. Update the config-network configuration to use the Traefik ingress class.

    ```bash
       kubectl patch configmap/config-network \
       -n knative-serving \
       --type merge \
       -p '{"data":{"ingress.class":"traefik.ingress.networking.knative.dev"}}'
    ```

4. Add a custom domain to your Knative configuration (Optional).

    ```bash
    kubectl patch configmap config-domain \
      -n knative-serving \
      --type='merge' \
      -p='{"data":{"example.com":""}}'
    ```

5. Install/update the Traefik [RBAC](https://raw.githubusercontent.com/traefik/traefik/473e27980fe40f447ada70783ae28aabae86107d/docs/content/reference/dynamic-configuration/kubernetes-knative-rbac.yml).

    ```bash
    kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.7/docs/content/reference/dynamic-configuration/kubernetes-knative-rbac.yml
    ```

## Configuration Example

As this provider is an experimental feature, it needs to be enabled in the experimental and in the provider sections of the configuration.
You can enable the Knative provider as detailed below:

**File (YAML)**

```yaml
experimental:
  knative: true

providers:
  knative: {}
```

**File (TOML)**

```toml
[experimental.knative]

[providers.knative]
```

**CLI**

```bash
--experimental.knative=true
--providers.knative=true
```

The Knative provider uses the Knative API to retrieve its routing configuration.
The provider then watches for incoming Knative events and derives the corresponding dynamic configuration from it.

## Configuration Options

<!-- markdownlint-disable MD013 -->

| Field                                                                                                                                                                                                    | Description                                                                                                                                                                                                                                                                                                                                                                          | Default | Required |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|:---------|
| <a id="opt-providers-providersThrottleDuration" href="#opt-providers-providersThrottleDuration" title="#opt-providers-providersThrottleDuration">`providers.providersThrottleDuration`</a> | Minimum amount of time to wait for, after a configuration reload, before taking into account any new configuration refresh event.<br />If multiple events occur within this time, only the most recent one is taken into account, and all others are discarded.<br />**This option cannot be set per provider, but the throttling algorithm applies to each of them independently.** | 2s      | No       |
| <a id="opt-providers-knative-endpoint" href="#opt-providers-knative-endpoint" title="#opt-providers-knative-endpoint">providers.knative.endpoint</a> | Server endpoint URL.<br />More information [here](#endpoint).                                                                                                                                                                                                                                                                                                                        |         |
| <a id="opt-providers-knative-token" href="#opt-providers-knative-token" title="#opt-providers-knative-token">providers.knative.token</a> | Bearer token used for the Kubernetes client configuration.                                                                                                                                                                                                                                                                                                                           |         |
| <a id="opt-providers-knative-certAuthFilePath" href="#opt-providers-knative-certAuthFilePath" title="#opt-providers-knative-certAuthFilePath">providers.knative.certAuthFilePath</a> | Path to the certificate authority file.<br />Used for the Kubernetes client configuration.                                                                                                                                                                                                                                                                                           |         |
| <a id="opt-providers-knative-namespaces" href="#opt-providers-knative-namespaces" title="#opt-providers-knative-namespaces">providers.knative.namespaces</a> | Array of namespaces to watch.<br />If left empty, watch all namespaces.                                                                                                                                                                                                                                                                                                              |         |
| <a id="opt-providers-knative-labelSelector" href="#opt-providers-knative-labelSelector" title="#opt-providers-knative-labelSelector">providers.knative.labelSelector</a> | Allow filtering Knative Ingress objects using label selectors.                                                                                                                                                                                                                                                                                                                       |         |
| <a id="opt-providers-knative-throttleDuration" href="#opt-providers-knative-throttleDuration" title="#opt-providers-knative-throttleDuration">providers.knative.throttleDuration</a> | Minimum amount of time to wait between two Kubernetes events before producing a new configuration.<br />This prevents a Kubernetes cluster that updates many times per second from continuously changing your Traefik configuration.<br />If empty, every event is caught.                                                                                                           | 0       |
| <a id="opt-providers-knative-privateEntrypoints" href="#opt-providers-knative-privateEntrypoints" title="#opt-providers-knative-privateEntrypoints">providers.knative.privateEntrypoints</a> | Entrypoint names used to expose the Ingress privately. If empty local Ingresses are skipped.                                                                                                                                                                                                                                                                                         |         |
| <a id="opt-providers-knative-privateService" href="#opt-providers-knative-privateService" title="#opt-providers-knative-privateService">providers.knative.privateService</a> | Kubernetes service used to expose the networking controller privately.                                                                                                                                                                                                                                                                                                               |         |
| <a id="opt-providers-knative-privateService-desc" href="#opt-providers-knative-privateService-desc" title="#opt-providers-knative-privateService-desc">providers.knative.privateService.desc</a> | Name of the private Kubernetes service.                                                                                                                                                                                                                                                                                                                                              |         |
| <a id="opt-providers-knative-privateService-namespace" href="#opt-providers-knative-privateService-namespace" title="#opt-providers-knative-privateService-namespace">providers.knative.privateService.namespace</a> | Namespace of the private Kubernetes service.                                                                                                                                                                                                                                                                                                                                         |         |
| <a id="opt-providers-knative-publicEntrypoints" href="#opt-providers-knative-publicEntrypoints" title="#opt-providers-knative-publicEntrypoints">providers.knative.publicEntrypoints</a> | Entrypoint names used to expose the Ingress publicly. If empty an Ingress is exposed on all entrypoints.                                                                                                                                                                                                                                                                             |         |
| <a id="opt-providers-knative-publicService" href="#opt-providers-knative-publicService" title="#opt-providers-knative-publicService">providers.knative.publicService</a> | Kubernetes service used to expose the networking controller publicly.                                                                                                                                                                                                                                                                                                                |         |
| <a id="opt-providers-knative-publicService-desc" href="#opt-providers-knative-publicService-desc" title="#opt-providers-knative-publicService-desc">providers.knative.publicService.desc</a> | Name of the public Kubernetes service.                                                                                                                                                                                                                                                                                                                                               |         |
| <a id="opt-providers-knative-publicService-namespace" href="#opt-providers-knative-publicService-namespace" title="#opt-providers-knative-publicService-namespace">providers.knative.publicService.namespace</a> | Namespace of the public Kubernetes service.                                                                                                                                                                                                                                                                                                                                          |         |

<!-- markdownlint-enable MD013 -->

### `endpoint`

The Kubernetes server endpoint URL.

When deployed into Kubernetes, Traefik reads the environment variables `KUBERNETES_SERVICE_HOST` and `KUBERNETES_SERVICE_PORT` or `KUBECONFIG` to construct the endpoint.

The access token is looked up in `/var/run/secrets/kubernetes.io/serviceaccount/token` and the SSL CA certificate in `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`.
Both are mounted automatically when deployed inside Kubernetes.

The endpoint may be specified to override the environment variable values inside a cluster.

When the environment variables are not found, Traefik tries to connect to the Knative API server with an external-cluster client.
In this case, the endpoint is required.
Specifically, it may be set to the URL used by `kubectl proxy` to connect to a Knative cluster using the granted authentication and authorization of the associated kubeconfig.

**File (YAML)**

```yaml
providers:
  knative:
    endpoint: "http://localhost:8080"
    # ...
```

**File (TOML)**

```toml
[providers.knative]
  endpoint = "http://localhost:8080"
  # ...
```

**CLI**

```bash
--providers.knative.endpoint=http://localhost:8080
```
## Routing Configuration

See the dedicated section in [routing](../../../routing-configuration/kubernetes/knative.md).

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
