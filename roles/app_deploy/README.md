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

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_applications` | List of applications to manage. See structure below. | `[]` |

Each application item supports:

| Variable | Description | Required |
|:---------|:------------|:---------|
| `name` | Logical application name (e.g. `myapp`) | Yes |
| `src` | Local path on the Ansible controller, or an `http(s)://` URL | Yes |
| `type` | Archive type: `war`, `ear`, `jar`. Inferred from the file extension when omitted. | No |
| `context_root` | Context-root override (e.g. `/myapp`). Written into `server.xml` in explicit mode. | No |
| `state` | `present` (default) or `absent` | No |
| `checksum` | `sha256:<hex>` checksum for URL downloads | No |

### Deployment mode

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_deploy_to_dropins` | `true` = dropins directory; `false` = explicit `<application>` in config | `false` |
| `openliberty_dropins_dir` | dropins sub-directory name (Liberty standard) | `dropins` |

### Server connection

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_home` | Liberty home directory | `/opt/openliberty/wlp` |
| `openliberty_server_name` | Target Liberty server instance | `defaultServer` |
| `openliberty_user` | File owner for deployed archives | `liberty` |
| `openliberty_group` | File group for deployed archives | `liberty` |
| `openliberty_http_port` | HTTP port used for readiness probes | `9080` |

### Deployment validation

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_deploy_validate` | Probe the app context root after deployment | `true` |
| `openliberty_deploy_wait_timeout` | Total seconds to wait for the app to respond | `120` |
| `openliberty_deploy_wait_delay` | Retry interval in seconds | `5` |

### Backup

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_deploy_backup` | Keep a timestamped `.bak` copy of replaced archives | `true` |

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

| Scenario | Description |
|:---------|:------------|
| [`app_deploy`](../../molecule/app_deploy/) | Deploy via configDropins, remove, re-deploy via dropins, backup |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
