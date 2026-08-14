# middleware_automation.open_liberty.version_update

In-place upgrade of an existing Open Liberty installation to a newer version.

The role:
1. Reads the currently installed version from `openliberty.properties`.
2. Skips the upgrade if the installed version already matches `openliberty_new_version`.
3. Stops the Liberty service.
4. Optionally backs up the existing `wlp/` directory.
5. Downloads the new Liberty archive from Maven Central (or a custom URL).
6. Removes the old `wlp/` tree and extracts the new archive.
7. Restarts the Liberty service.

Server configuration files (`server.xml`, `jvm.options`, `bootstrap.properties`) in
`wlp/usr/servers/` are preserved because they live outside the `wlp/` binary tree.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Open Liberty already installed by the [`install`](../install/README.md) role
- `become: true` (root privileges)
- Internet access to Maven Central, or a pre-staged archive URL

## Role Variables

### Target version

| Variable | Default | Description |
|---|---|---|
| `openliberty_new_version` | `"24.0.0.9"` | Target version to upgrade to |
| `openliberty_edition` | `webProfile` | Edition (must match the originally installed edition) |

### Paths and ownership

| Variable | Default | Description |
|---|---|---|
| `openliberty_install_dir` | `/opt/openliberty` | Base installation directory |
| `openliberty_home` | `/opt/openliberty/wlp` | Liberty home directory |
| `openliberty_install_workdir` | `/tmp` | Temporary directory for downloading the archive |
| `openliberty_user` | `liberty` | File owner |
| `openliberty_group` | `liberty` | File group |

### Download

| Variable | Default | Description |
|---|---|---|
| `openliberty_download_base_url` | `"https://repo1.maven.org/maven2/io/openliberty"` | Maven Central base URL |
| `openliberty_download_url` | `""` | Full override URL (bypasses Maven Central lookup) |
| `openliberty_download_checksum` | `""` | Optional `sha256:<hex>` checksum for the archive |
| `openliberty_download_retries` | `3` | Download retry attempts |
| `openliberty_download_timeout` | `600` | Seconds per download attempt |

### Backup

| Variable | Default | Description |
|---|---|---|
| `openliberty_update_backup` | `true` | Back up `wlp/` to `{{ openliberty_install_dir }}/wlp.backup.<timestamp>` before upgrade |

### Service

| Variable | Default | Description |
|---|---|---|
| `openliberty_service_name` | `openliberty-{{ openliberty_server_name }}` | systemd unit to stop/start during upgrade |
| `openliberty_server_name` | `defaultServer` | Liberty server name |
| `openliberty_java_home` | `/usr/lib/jvm/java-17-openjdk` | Java home |

## Dependencies

[`middleware_automation.open_liberty.install`](../install/README.md)

## Example Playbook

### Single-host upgrade

```yaml
- name: Upgrade Open Liberty
  hosts: liberty_servers
  vars:
    openliberty_new_version: "24.0.0.12"
    openliberty_edition: webProfile
    openliberty_update_backup: true
  roles:
    - role: middleware_automation.open_liberty.version_update
  post_tasks:
    - name: Validate after upgrade
      ansible.builtin.include_role:
        name: middleware_automation.open_liberty.validation
```

### Rolling upgrade (one host at a time)

```yaml
- name: Rolling upgrade of Open Liberty fleet
  hosts: liberty_servers
  serial: 1
  vars:
    openliberty_new_version: "24.0.0.12"
  roles:
    - role: middleware_automation.open_liberty.version_update
```

### Use an internal mirror

```yaml
vars:
  openliberty_new_version: "24.0.0.12"
  openliberty_download_url: "https://nexus.internal/liberty/openliberty-webProfile10-24.0.0.12.zip"
  openliberty_download_checksum: "sha256:deadbeef..."
```

## Molecule Tests

| Scenario | What is tested |
|---|---|
| [`version_update`](../../molecule/version_update/) | Upgrade from 24.0.0.9 → 24.0.0.12, verify new version, backup directory, service active |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
