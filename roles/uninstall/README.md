# middleware_automation.open_liberty.uninstall

Completely remove an Open Liberty installation from the target host.

The role:
1. Stops and disables the Liberty systemd service.
2. Removes the systemd unit file and reloads the daemon.
3. Deletes the Liberty installation directory (including `wlp/` and all server data).
4. Optionally removes the `liberty` system user and group.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- `become: true` (root privileges)

## Role Variables

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_service_name` | systemd unit to stop and remove | `openliberty-{{ openliberty_server_name }}` |
| `openliberty_server_name` | Liberty server name (used to derive the unit name) | `defaultServer` |
| `openliberty_install_dir` | Installation directory to delete | `/opt/openliberty` |
| `openliberty_user` | System user to remove | `liberty` |
| `openliberty_group` | System group to remove | `liberty` |
| `openliberty_remove_user` | Remove the system user when `true` | `true` |
| `openliberty_remove_group` | Remove the system group when `true` | `true` |

## Dependencies

None. The role is intentionally self-contained so it can be run against hosts
where the install role may have partially completed.

## Example Playbook

### Standard uninstall

```yaml
- name: Remove Open Liberty
  hosts: liberty_servers
  vars:
    openliberty_server_name: defaultServer
    openliberty_remove_user: true
    openliberty_remove_group: true
  roles:
    - role: middleware_automation.open_liberty.uninstall
```

### Preserve the system user (managed externally)

```yaml
- name: Remove Open Liberty but keep liberty user
  hosts: liberty_servers
  vars:
    openliberty_remove_user: false
    openliberty_remove_group: false
  roles:
    - role: middleware_automation.open_liberty.uninstall
```

### Custom server name

```yaml
- name: Remove custom Liberty instance
  hosts: liberty_servers
  vars:
    openliberty_server_name: appServer
    openliberty_install_dir: /opt/openliberty
  roles:
    - role: middleware_automation.open_liberty.uninstall
```

## Molecule Tests

| Scenario | Description |
|:---------|:------------|
| [`uninstall`](../../molecule/uninstall/) | Full install then uninstall — asserts install dir, unit file, user, group, and port are all gone |
| [`default`](../../molecule/default/) | Used as the cleanup step |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
