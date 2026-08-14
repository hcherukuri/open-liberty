# middleware_automation.open_liberty.install

Download, verify, and extract an [IBM Open Liberty](https://openliberty.io/) archive on the target host.
Creates a dedicated system user and group, and installs Java if requested.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- `become: true` (root privileges)
- `unzip` package (installed automatically by this role)
- Internet access to Maven Central, or a pre-staged archive URL via `openliberty_download_url`

## Role Variables

### Version and edition

| Variable | Default | Description |
|---|---|---|
| `openliberty_version` | `"24.0.0.9"` | Open Liberty version to install |
| `openliberty_edition` | `"webProfile"` | Edition: `kernel`, `webProfile`, `jakartaee`, `microProfile` |

### Download

| Variable | Default | Description |
|---|---|---|
| `openliberty_download_base_url` | `"https://repo1.maven.org/maven2/io/openliberty"` | Base URL for Maven Central archives |
| `openliberty_download_url` | `""` | Full override URL; when set, `download_base_url` is ignored |
| `openliberty_download_checksum` | `""` | Optional `sha256:<hex>` checksum for the archive |
| `openliberty_download_retries` | `3` | Number of download retry attempts |
| `openliberty_download_timeout` | `600` | Seconds per download attempt |
| `openliberty_install_workdir` | `/tmp` | Temporary directory for the downloaded archive |

### Installation path

| Variable | Default | Description |
|---|---|---|
| `openliberty_install_dir` | `/opt/openliberty` | Base installation directory |
| `openliberty_home` | `{{ openliberty_install_dir }}/wlp` | Liberty home (`wlp/`) — computed, override only if non-standard |

### System user

| Variable | Default | Description |
|---|---|---|
| `openliberty_user` | `liberty` | System user that owns the installation |
| `openliberty_group` | `liberty` | System group |
| `openliberty_manage_user` | `true` | Set to `false` if the user is managed externally |
| `openliberty_user_shell` | `/sbin/nologin` | Login shell for the service account |

### Java

| Variable | Default | Description |
|---|---|---|
| `openliberty_install_java` | `false` | When `true`, installs the default Java package for the OS |
| `openliberty_java_home` | `/usr/lib/jvm/java-17-openjdk` | Java home passed to Liberty at runtime |

## Dependencies

None.

## Example Playbook

```yaml
- name: Install Open Liberty
  hosts: liberty_servers
  vars:
    openliberty_version: "24.0.0.9"
    openliberty_edition: webProfile
    openliberty_install_java: true
    openliberty_java_home: /usr/lib/jvm/java-17-openjdk
  roles:
    - role: middleware_automation.open_liberty.install
```

### Use a local mirror

```yaml
vars:
  openliberty_download_url: "https://nexus.internal/liberty/openliberty-webProfile10-24.0.0.9.zip"
  openliberty_download_checksum: "sha256:abc123..."
```

## Molecule Tests

This role is covered by the following Molecule scenarios:

| Scenario | What is tested |
|---|---|
| [`default`](../../molecule/default/) | webProfile install on RHEL 8, 9, and 10 |
| [`microprofile`](../../molecule/microprofile/) | MicroProfile edition install |
| [`app_deploy`](../../molecule/app_deploy/) | Install as prerequisite for deployment tests |
| [`port_config`](../../molecule/port_config/) | Install as prerequisite for port reconfiguration |
| [`version_update`](../../molecule/version_update/) | Install initial version before upgrade |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
