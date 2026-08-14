# middleware_automation.open_liberty.port_config

Reconfigure the HTTP and HTTPS listener ports on a running Open Liberty server.
Writes a `configDropins/overrides/port_config.xml` override file and optionally
opens the new ports in firewalld/ufw.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Open Liberty installed and running
  (see [`install`](../install/README.md), [`server_config`](../server_config/README.md), [`systemd`](../systemd/README.md))
- `become: true` (root privileges)
- `ansible.posix` collection (for firewalld) when `openliberty_firewall_port_manage: true`

## Role Variables

### Server connection

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_home` | Liberty home directory | `/opt/openliberty/wlp` |
| `openliberty_server_name` | Server instance to reconfigure | `defaultServer` |
| `openliberty_user` | Owner of the generated XML override file | `liberty` |
| `openliberty_group` | Group of the generated XML override file | `liberty` |
| `openliberty_service_name` | systemd unit to restart after reconfiguration | `openliberty-{{ openliberty_server_name }}` |

### HTTP endpoint

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_http_port` | HTTP port (`-1` to disable) | `9080` |
| `openliberty_https_port` | HTTPS port (`-1` to disable) | `9443` |
| `openliberty_https_enabled` | Enable the HTTPS listener (requires SSL/keystore configuration for production) | `false` |
| `openliberty_endpoint_host` | Network interface to bind; `"*"` = all interfaces | `"*"` |
| `openliberty_endpoint_id` | `<httpEndpoint>` element ID in `server.xml` | `defaultHttpEndpoint` |

### HTTP options

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_http_max_keep_alive_requests` | Max persistent requests per connection (0 = unlimited) | `100` |
| `openliberty_http_persist_timeout` | Keep-alive timeout in seconds (-1 = client timeout) | `30` |

### Firewall management

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_firewall_port_manage` | Open firewall ports automatically | `false` |
| `openliberty_firewall_zone` | firewalld zone (RHEL only) | `public` |

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
    openliberty_firewall_port_manage: false
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
    openliberty_firewall_port_manage: true
    openliberty_firewall_zone: internal
  roles:
    - role: middleware_automation.open_liberty.port_config
```

## Molecule Tests

| Scenario | Description |
|:---------|:------------|
| [`port_config`](../../molecule/port_config/) | Reconfigure from 9080→8080, verify new port open and old port closed |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
