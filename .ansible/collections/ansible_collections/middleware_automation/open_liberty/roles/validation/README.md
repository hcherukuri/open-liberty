# middleware_automation.open_liberty.validation

Assert that an Open Liberty server is running and healthy after installation or configuration.

The role performs three checks in order:

1. **Service check** — asserts that the systemd service is in the `active` state.
2. **Port wait** — waits until the HTTP port is accepting connections.
3. **Health endpoint** *(optional)* — queries an HTTP health URL and asserts an HTTP 200 response.
   Requires the `mpHealth` feature (included in the `microProfile` edition by default).

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Open Liberty installed, configured, and started
- `become: true` (for systemd status queries)

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `openliberty_server_name` | `defaultServer` | Liberty server name |
| `openliberty_service_name` | `openliberty-{{ openliberty_server_name }}` | systemd unit to check |
| `openliberty_home` | `/opt/openliberty/wlp` | Liberty home directory |
| `openliberty_http_port` | `9080` | HTTP port to wait on |
| `openliberty_validation_timeout` | `300` | Total seconds to wait for the server |
| `openliberty_validation_delay` | `10` | Seconds between retry attempts |
| `openliberty_validate_health_endpoint` | `true` | Perform an HTTP health check when `true` |
| `openliberty_health_url_path` | `"/health"` | URL path for the health check (requires `mpHealth` feature) |

## Dependencies

- [`middleware_automation.open_liberty.install`](../install/README.md)
- [`middleware_automation.open_liberty.server_config`](../server_config/README.md)
- [`middleware_automation.open_liberty.systemd`](../systemd/README.md)

## Example Playbook

### Full installation with validation

```yaml
- name: Install and validate Open Liberty
  hosts: liberty_servers
  vars:
    openliberty_version: "24.0.0.9"
    openliberty_edition: webProfile
    openliberty_validate_health_endpoint: false   # webProfile has no /health
  roles:
    - role: middleware_automation.open_liberty.install
    - role: middleware_automation.open_liberty.server_config
    - role: middleware_automation.open_liberty.systemd
    - role: middleware_automation.open_liberty.validation
```

### MicroProfile with /health endpoint check

```yaml
- name: Install MicroProfile Liberty and check /health
  hosts: liberty_servers
  vars:
    openliberty_edition: microProfile
    openliberty_validate_health_endpoint: true
    openliberty_health_url_path: "/health"
    openliberty_validation_timeout: 300
  roles:
    - role: middleware_automation.open_liberty.install
    - role: middleware_automation.open_liberty.server_config
    - role: middleware_automation.open_liberty.systemd
    - role: middleware_automation.open_liberty.validation
```

### Validate an already-running server

```yaml
- name: Validate Liberty is healthy
  hosts: liberty_servers
  vars:
    openliberty_validate_health_endpoint: false
  roles:
    - role: middleware_automation.open_liberty.validation
```

## Molecule Tests

| Scenario | What is tested |
|---|---|
| [`validation`](../../molecule/validation/) | Service check, port wait, and `/health` endpoint (microProfile edition) |
| [`default`](../../molecule/default/) | `openliberty_validate_health_endpoint: false` path |
| [`microprofile`](../../molecule/microprofile/) | Full `/health` endpoint check |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
