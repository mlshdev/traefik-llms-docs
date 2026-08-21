---
title: "Traefik DigestAuth Documentation"
description: "Traefik Proxy's HTTP DigestAuth middleware restricts access to your services to known users. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / DigestAuth"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/digestauth.md"
source_url: "https://github.com/traefik/traefik/blob/b78307590625ada3e430d358b7947f11a0aef226/docs/content/reference/routing-configuration/http/middlewares/digestauth.md"
---

The `DigestAuth` middleware grants access to services to authorized users only.

## Configuration Examples

**Structured (YAML)**

```yaml
# Declaring the user list
http:
  middlewares:
    test-auth:
      digestAuth:
        users:
          - "test:traefik:a2688e031edb4be6a3797f3882655c05"
          - "test2:traefik:518845800f9e2bfb1f1f740ec24f074e"
```

**Structured (TOML)**

```toml
# Declaring the user list
[http.middlewares]
  [http.middlewares.test-auth.digestAuth]
    users = [
      "test:traefik:a2688e031edb4be6a3797f3882655c05",
      "test2:traefik:518845800f9e2bfb1f1f740ec24f074e",
    ]
```

**Labels**

```yaml
# Declaring the user list
labels:
  - "traefik.http.middlewares.test-auth.digestauth.users=test:traefik:a2688e031edb4be6a3797f3882655c05,test2:traefik:518845800f9e2bfb1f1f740ec24f074e"
```

**Tags**

```json
// Declaring the user list
{
  //...
  "Tags" : [
    "traefik.http.middlewares.test-auth.digestauth.users=test:traefik:a2688e031edb4be6a3797f3882655c05,test2:traefik:518845800f9e2bfb1f1f740ec24f074e"
  ]
}
```

**Kubernetes**

```yaml
# Declaring the user list
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: test-auth
spec:
  digestAuth:
    secret: userssecret
```

## Configuration Options

| Field      | Description    | Default | Required |
|:-----------|:---------------------------------------------------------------------------------|:--------|:---------|
| <a id="opt-users" href="#opt-users" title="#opt-users">`users`</a> | Array of authorized users. Each user must be declared using the `name:realm:encoded-password` format.<br /> The option `users` supports Kubernetes secrets.<br />(More information [here](#users--usersfile))| []  | No      |
| <a id="opt-usersFile" href="#opt-usersFile" title="#opt-usersFile">`usersFile`</a> | Path to an external file that contains the authorized users for the middleware. <br />The file content is a list of `name:realm:encoded-password`. (More information [here](#users--usersfile)) | ""      | No      |
| <a id="opt-realm" href="#opt-realm" title="#opt-realm">`realm`</a> | Allow customizing the realm for the authentication.| "traefik"      | No      |
| <a id="opt-headerField" href="#opt-headerField" title="#opt-headerField">`headerField`</a> | Allow defining a header field to store the authenticated user.| ""      | No      |
| <a id="opt-removeHeader" href="#opt-removeHeader" title="#opt-removeHeader">`removeHeader`</a> | Allow removing the authorization header before forwarding the request to your service. | false      | No      |

### Passwords format

Use `htdigest` to generate the passwords.

### users & usersFile

- If both `users` and `usersFile` are provided, they are merged. The values in `users` have precedence over the contents of `usersFile`.
- Because referencing a file path isn’t feasible on Kubernetes, the `users` & `usersFile` field isn’t used in Kubernetes IngressRoute. Instead, use the `secret` field.

### Kubernetes Secrets

On Kubernetes, you don’t use the `users` or `usersFile` fields. Instead, you reference a Kubernetes secret using the `secret` field in your Middleware resource. This secret can be one of two types:

- `kubernetes.io/basic-auth secret`: This secret type contains two keys—`username` and `password`—but is generally suited for a smaller number of users. Please note that these keys are not hashed or encrypted in any way, and therefore is less secure than the other method.
- Opaque secret with a users field: Here, the secret contains a single string field (often called `users`) where each line represents a user. This approach allows you to store multiple users in one secret.

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
