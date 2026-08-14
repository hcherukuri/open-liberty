# middleware_automation.open_liberty.systemd

Deploy a systemd service unit for Open Liberty and manage the service lifecycle
(start, stop, enable on boot).

JVM options are managed by the [`server_config`](../server_config/README.md) role
via `jvm.options` (`openliberty_jvm_options`). This role does not set `JVM_ARGS`.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Open Liberty installed and configured (see [`install`](../install/README.md) and [`server_config`](../server_config/README.md))
- `become: true` (root privileges)
- systemd on the target host

## Role Variables

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_service_name` | systemd unit name | `openliberty-{{ openliberty_server_name }}` |
| `openliberty_service_state` | Desired service state: `started`, `stopped`, `restarted` | `started` |
| `openliberty_service_enabled` | Enable the service to start on boot | `true` |
| `openliberty_service_start_timeout` | Seconds systemd allows for the service to start | `300` |
| `openliberty_server_name` | Liberty server name (used to derive the unit name) | `defaultServer` |
| `openliberty_home` | Liberty home directory | `/opt/openliberty/wlp` |
| `openliberty_user` | User the service runs as | `liberty` |
| `openliberty_group` | Group the service runs as | `liberty` |
| `openliberty_java_home` | `JAVA_HOME` exported in the service environment | `/usr/lib/jvm/java-17-openjdk` |
| `openliberty_service_env_vars` | Extra environment variables. Each item: `key`, `value` | `[]` |

## Dependencies

- [`middleware_automation.open_liberty.install`](../install/README.md)
- [`middleware_automation.open_liberty.server_config`](../server_config/README.md)

## Example Playbook

### Default — start and enable on boot

```yaml
- name: Install and start Open Liberty
  hosts: liberty_servers
  roles:
    - role: middleware_automation.open_liberty.install
    - role: middleware_automation.open_liberty.server_config
    - role: middleware_automation.open_liberty.systemd
```

### Custom service with extra environment variables

```yaml
- name: Start Liberty with custom environment
  hosts: liberty_servers
  vars:
    openliberty_server_name: appServer
    openliberty_service_env_vars:
      - key: WLP_OUTPUT_DIR
        value: /var/log/openliberty
  roles:
    - role: middleware_automation.open_liberty.systemd
```

## Molecule Tests

| Scenario | Description |
|:---------|:------------|
| [`default`](../../molecule/default/) | Service unit on RHEL 8, 9, and 10, service is active |
| [`microprofile`](../../molecule/microprofile/) | Custom service name (`openliberty-microServer`) |
| [`app_deploy`](../../molecule/app_deploy/) | Service running before deployment tests |
| [`port_config`](../../molecule/port_config/) | Service restart after port reconfiguration |
| [`version_update`](../../molecule/version_update/) | Service restart after version upgrade |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
