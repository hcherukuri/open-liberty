# middleware_automation.open_liberty.version_update

In-place upgrade of an existing Open Liberty installation to a newer version.

The role:
1. Reads the currently installed version from `openliberty.properties`.
2. Fails if `openliberty_new_version` would downgrade the installation.
3. Skips the upgrade if the installed version is already greater than or equal to `openliberty_new_version`.
4. Stops the Liberty service.
5. Optionally backs up the existing `wlp/` directory.
6. Downloads the new Liberty archive from Maven Central (or a custom URL).
7. Removes the old `wlp/` tree and extracts the new archive.
8. Rolls back from the backup if the upgrade fails.
9. Restarts the Liberty service.

Server configuration files (`server.xml`, `jvm.options`, `bootstrap.properties`) under
`wlp/usr/servers/` should be re-applied with the `server_config` role after upgrade when
needed. Enable `openliberty_update_backup` so a failed upgrade can roll back.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Open Liberty already installed by the [`install`](../install/README.md) role
- `become: true` (root privileges)
- Internet access to Maven Central, or a pre-staged archive URL

## Role Variables

### Target version

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_new_version` | Target version to upgrade to (must be newer than installed) | `"24.0.0.9"` |
| `openliberty_edition` | Edition (must match the originally installed edition) | `webProfile` |

### Paths and ownership

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_install_dir` | Base installation directory | `/opt/openliberty` |
| `openliberty_home` | Liberty home directory | `/opt/openliberty/wlp` |
| `openliberty_install_workdir` | Temporary directory for downloading the archive | `/tmp` |
| `openliberty_user` | File owner | `liberty` |
| `openliberty_group` | File group | `liberty` |

### Download

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_download_base_url` | Maven Central base URL | `"https://repo1.maven.org/maven2/io/openliberty"` |
| `openliberty_download_url` | Full override URL (bypasses Maven Central lookup) | `""` |
| `openliberty_download_checksum` | Optional `sha256:<hex>` checksum for the archive | `""` |
| `openliberty_download_retries` | Download retry attempts | `3` |
| `openliberty_download_timeout` | Seconds per download attempt | `600` |

### Backup

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_update_backup` | Back up `wlp/` to `{{ openliberty_install_dir }}/wlp.backup.<timestamp>` before upgrade | `true` |

### Service

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_service_name` | systemd unit to stop/start during upgrade | `openliberty-{{ openliberty_server_name }}` |
| `openliberty_server_name` | Liberty server name | `defaultServer` |

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

| Scenario | Description |
|:---------|:------------|
| [`version_update`](../../molecule/version_update/) | Upgrade from 24.0.0.9 → 24.0.0.12, verify new version, backup directory, service active, and that a downgrade attempt fails |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
