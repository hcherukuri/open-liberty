# middleware_automation.open_liberty.app_deploy

Deploy WAR, EAR, or JAR application archives to a running Open Liberty server.
Supports two deployment modes:

- **dropins** — copy the archive to the `dropins/` directory; Liberty auto-discovers it.
- **explicit** — write an `<application>` element into `configDropins/overrides/app_deploy.xml`; gives full control over context root and type.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Open Liberty installed, configured, and running
  (see [`install`](../install/README.md), [`server_config`](../server_config/README.md), [`systemd`](../systemd/README.md))
- `become: true` (root privileges)

## Role Variables

### Application list

| Variable | Default | Description |
|---|---|---|
| `openliberty_applications` | `[]` | List of applications to manage. See structure below. |

Each application item supports:

| Key | Required | Description |
|---|---|---|
| `name` | ✅ | Logical application name (e.g. `myapp`) |
| `src` | ✅ | Local path on the Ansible controller, or an `http(s)://` URL |
| `type` | ❌ | Archive type: `war`, `ear`, `jar`. Inferred from the file extension when omitted. |
| `context_root` | ❌ | Context-root override (e.g. `/myapp`). Written into `server.xml` in explicit mode. |
| `state` | ❌ | `present` (default) or `absent` |
| `checksum` | ❌ | `sha256:<hex>` checksum for URL downloads |

### Deployment mode

| Variable | Default | Description |
|---|---|---|
| `openliberty_deploy_to_dropins` | `false` | `true` = dropins directory; `false` = explicit `<application>` in config |
| `openliberty_dropins_dir` | `dropins` | dropins sub-directory name (Liberty standard) |

### Server connection

| Variable | Default | Description |
|---|---|---|
| `openliberty_home` | `/opt/openliberty/wlp` | Liberty home directory |
| `openliberty_server_name` | `defaultServer` | Target Liberty server instance |
| `openliberty_user` | `liberty` | File owner for deployed archives |
| `openliberty_group` | `liberty` | File group for deployed archives |
| `openliberty_http_port` | `9080` | HTTP port used for readiness probes |

### Deployment validation

| Variable | Default | Description |
|---|---|---|
| `openliberty_deploy_validate` | `true` | Probe the app context root after deployment |
| `openliberty_deploy_wait_timeout` | `120` | Total seconds to wait for the app to respond |
| `openliberty_deploy_wait_delay` | `5` | Retry interval in seconds |

### Backup

| Variable | Default | Description |
|---|---|---|
| `openliberty_deploy_backup` | `true` | Keep a timestamped `.bak` copy of replaced archives |

## Dependencies

- [`middleware_automation.open_liberty.install`](../install/README.md)
- [`middleware_automation.open_liberty.server_config`](../server_config/README.md)
- [`middleware_automation.open_liberty.systemd`](../systemd/README.md)

## Example Playbook

### Deploy via dropins (auto-discovery)

```yaml
- name: Deploy application to Open Liberty dropins
  hosts: liberty_servers
  vars:
    openliberty_deploy_to_dropins: true
    openliberty_applications:
      - name: myapp
        src: /builds/myapp-1.0.war
        state: present
  roles:
    - role: middleware_automation.open_liberty.app_deploy
```

### Deploy with explicit server.xml entry

```yaml
- name: Deploy application with context root
  hosts: liberty_servers
  vars:
    openliberty_applications:
      - name: myapp
        src: /builds/myapp-1.0.war
        context_root: /myapp
        state: present
      - name: adminapp
        src: https://nexus.internal/releases/admin-2.0.ear
        checksum: "sha256:deadbeef..."
        state: present
  roles:
    - role: middleware_automation.open_liberty.app_deploy
```

### Remove an application

```yaml
- name: Remove application from Liberty
  hosts: liberty_servers
  vars:
    openliberty_applications:
      - name: myapp
        src: /builds/myapp-1.0.war
        state: absent
  roles:
    - role: middleware_automation.open_liberty.app_deploy
```

## Molecule Tests

| Scenario | What is tested |
|---|---|
| [`app_deploy`](../../molecule/app_deploy/) | Deploy via configDropins, remove, re-deploy via dropins, backup |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
