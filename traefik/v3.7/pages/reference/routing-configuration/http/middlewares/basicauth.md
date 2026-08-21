---
title: "Traefik BasicAuth Documentation"
description: "The HTTP basic authentication (BasicAuth) middleware in Traefik Proxy restricts access to your Services to known users. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / BasicAuth"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/basicauth.md"
source_url: "https://github.com/traefik/traefik/blob/b78307590625ada3e430d358b7947f11a0aef226/docs/content/reference/routing-configuration/http/middlewares/basicauth.md"
---

The `basicAuth` middleware grants access to services to authorized users only.

## Configuration Examples

**Structured (YAML)**

```yaml
# Declaring the user list
http:
  middlewares:
    test-auth:
      basicAuth:
        users:
          - "test:$apr1$H6uskkkW$IgXLP6ewTrSuBkTrqE8wj/"
          - "test2:$apr1$d9hr9HBB$4HxwgUir3HP4EsggP/QNo0"
```

**Structured (TOML)**

```toml
# Declaring the user list
[http.middlewares]
  [http.middlewares.test-auth.basicAuth]
  users = [
    "test:$apr1$H6uskkkW$IgXLP6ewTrSuBkTrqE8wj/",
    "test2:$apr1$d9hr9HBB$4HxwgUir3HP4EsggP/QNo0",
  ]
```

**Labels**

```yaml
# Declaring the user list
#
# Note: when used in docker-compose.yml all dollar signs in the hash need to be doubled for escaping.
# To create user:password pair, it's possible to use this command:
# echo $(htpasswd -nB user) | sed -e s/\\$/\\$\\$/g
#
# Also, note that dollar signs should NOT be doubled when not evaluated (e.g. Ansible docker_container module).
labels:
  - "traefik.http.middlewares.test-auth.basicauth.users=test:$$apr1$$H6uskkkW$$IgXLP6ewTrSuBkTrqE8wj/,test2:$$apr1$$d9hr9HBB$$4HxwgUir3HP4EsggP/QNo0"
```

**Tags**

```json
{
  // ...
  "Tags": [
    "traefik.http.middlewares.test-auth.basicauth.users=test:$apr1$H6uskkkW$IgXLP6ewTrSuBkTrqE8wj/,test2:$apr1$d9hr9HBB$4HxwgUir3HP4EsggP/QNo0"
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
  basicAuth:
    secret: secretName
```

## Configuration Options

| Field      | Description                                                                                                                                                                                 | Default | Required |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|:---------|
| <a id="opt-users" href="#opt-users" title="#opt-users">`users`</a> | Array of authorized users. Each user must be declared using the `name:hashed-password` format. (More information [here](#users-usersfile))| ""      | No      |
| <a id="opt-usersFile" href="#opt-usersFile" title="#opt-usersFile">`usersFile`</a> | Path to an external file that contains the authorized users for the middleware. <br />The file content is a list of `name:hashed-password`. (More information [here](#users-usersfile)) | ""      | No      |
| <a id="opt-realm" href="#opt-realm" title="#opt-realm">`realm`</a> | Allow customizing the realm for the authentication.| "traefik"      | No      |
| <a id="opt-headerField" href="#opt-headerField" title="#opt-headerField">`headerField`</a> | Allow defining a header field to store the authenticated user.| ""      | No      |
| <a id="opt-removeHeader" href="#opt-removeHeader" title="#opt-removeHeader">`removeHeader`</a> | Allow removing the authorization header before forwarding the request to your service. | false      | No      |

### Passwords format

Passwords must be hashed using MD5, SHA1, or BCrypt.
Use `htpasswd` to generate the passwords.

### users & usersFile

- If both `users` and `usersFile` are provided, they are merged. The values in `users` have precedence over the contents of `usersFile`.
- Because referencing a file path isn’t feasible on Kubernetes, the `users` & `usersFile` field isn’t used in Kubernetes IngressRoute. Instead, use the `secret` field.

#### Kubernetes Secrets

The option `users` supports Kubernetes secrets.

> **Note — Kubernetes `kubernetes.io/basic-auth` secret type**
>
> Kubernetes supports a special `kubernetes.io/basic-auth` secret type.
> This secret must contain two keys: `username` and `password`.
>
> Please note that these keys are not hashed or encrypted in any way, and therefore is less secure than other methods.
> You can find more information on the [Kubernetes Basic Authentication Secret Documentation](https://kubernetes.io/docs/concepts/configuration/secret/#basic-authentication-secret)

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
