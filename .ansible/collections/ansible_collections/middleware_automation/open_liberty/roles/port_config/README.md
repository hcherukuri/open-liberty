# middleware_automation.open_liberty.port_config

Reconfigure the HTTP and HTTPS listener ports on a running Open Liberty server.
Writes a `configDropins/overrides/port_config.xml` override file and optionally
opens the new ports in firewalld.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Open Liberty installed and running
  (see [`install`](../install/README.md), [`server_config`](../server_config/README.md), [`systemd`](../systemd/README.md))
- `become: true` (root privileges)
- `ansible.posix` collection (for firewalld) when `openliberty_port_manage_firewall: true`

## Role Variables

### Server connection

| Variable | Default | Description |
|---|---|---|
| `openliberty_home` | `/opt/openliberty/wlp` | Liberty home directory |
| `openliberty_server_name` | `defaultServer` | Server instance to reconfigure |
| `openliberty_user` | `liberty` | Owner of the generated XML override file |
| `openliberty_group` | `liberty` | Group of the generated XML override file |
| `openliberty_service_name` | `openliberty-{{ openliberty_server_name }}` | systemd unit to restart after reconfiguration |

### HTTP endpoint

| Variable | Default | Description |
|---|---|---|
| `openliberty_http_port` | `9080` | HTTP port (`-1` to disable) |
| `openliberty_https_port` | `9443` | HTTPS port (`-1` to disable) |
| `openliberty_https_enabled` | `true` | Enable the HTTPS listener |
| `openliberty_endpoint_host` | `"*"` | Network interface to bind; `"*"` = all interfaces |
| `openliberty_endpoint_id` | `defaultHttpEndpoint` | `<httpEndpoint>` element ID in `server.xml` |

### HTTP options

| Variable | Default | Description |
|---|---|---|
| `openliberty_http_max_keep_alive_requests` | `100` | Max persistent requests per connection (0 = unlimited) |
| `openliberty_http_persist_timeout` | `30` | Keep-alive timeout in seconds (-1 = client timeout) |

### Firewall management

| Variable | Default | Description |
|---|---|---|
| `openliberty_port_manage_firewall` | `false` | Open firewall ports automatically |
| `openliberty_firewall_zone` | `public` | firewalld zone (RHEL only) |

## Dependencies

- [`middleware_automation.open_liberty.install`](../install/README.md)
- [`middleware_automation.open_liberty.server_config`](../server_config/README.md)
- [`middleware_automation.open_liberty.systemd`](../systemd/README.md)

## Example Playbook

### Reconfigure ports (no firewall)

```yaml
- name: Reconfigure Liberty to listen on 8080/8443
  hosts: liberty_servers
  vars:
    openliberty_http_port: 8080
    openliberty_https_port: 8443
    openliberty_https_enabled: true
    openliberty_port_manage_firewall: false
  roles:
    - role: middleware_automation.open_liberty.port_config
```

### Reconfigure ports and update firewalld

```yaml
- name: Move Liberty to port 8080, open firewall
  hosts: liberty_servers
  vars:
    openliberty_http_port: 8080
    openliberty_https_enabled: false
    openliberty_port_manage_firewall: true
    openliberty_firewall_zone: internal
  roles:
    - role: middleware_automation.open_liberty.port_config
```

## Molecule Tests

| Scenario | What is tested |
|---|---|
| [`port_config`](../../molecule/port_config/) | Reconfigure from 9080→8080, verify new port open and old port closed |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
