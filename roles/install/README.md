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

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_version` | Open Liberty version to install | `"24.0.0.9"` |
| `openliberty_edition` | Edition: `kernel`, `webProfile`, `jakartaee`, `microProfile` | `"webProfile"` |

### Download

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_download_base_url` | Base URL for Maven Central archives | `"https://repo1.maven.org/maven2/io/openliberty"` |
| `openliberty_download_url` | Full override URL; when set, `download_base_url` is ignored | `""` |
| `openliberty_download_checksum` | Optional `sha256:<hex>` checksum for the archive | `""` |
| `openliberty_download_retries` | Number of download retry attempts | `3` |
| `openliberty_download_timeout` | Seconds per download attempt | `600` |
| `openliberty_install_workdir` | Temporary directory for the downloaded archive | `/tmp` |

### Installation path

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_install_dir` | Base installation directory | `/opt/openliberty` |
| `openliberty_home` | Liberty home (`wlp/`) — computed, override only if non-standard | `{{ openliberty_install_dir }}/wlp` |

### System user

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_user` | System user that owns the installation | `liberty` |
| `openliberty_group` | System group | `liberty` |
| `openliberty_manage_user` | Set to `false` if the user is managed externally | `true` |
| `openliberty_user_shell` | Login shell for the service account | `/sbin/nologin` |

### Java

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_install_java` | When `true`, installs OpenJDK (`openliberty_java_version`) | `false` |
| `openliberty_java_version` | OpenJDK major version to install (use `"21"` on RHEL 10) | `"17"` |
| `openliberty_java_home` | JAVA_HOME; discovered automatically when install_java is true | `/usr/lib/jvm/java-17-openjdk` |

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

| Scenario | Description |
|:---------|:------------|
| [`default`](../../molecule/default/) | webProfile install on RHEL 8, 9, and 10 |
| [`microprofile`](../../molecule/microprofile/) | MicroProfile edition install |
| [`app_deploy`](../../molecule/app_deploy/) | Install as prerequisite for deployment tests |
| [`port_config`](../../molecule/port_config/) | Install as prerequisite for port reconfiguration |
| [`version_update`](../../molecule/version_update/) | Install initial version before upgrade |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
