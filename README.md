# Ansible Collection: Open Liberty

[![License: GPL v2](https://img.shields.io/badge/License-GPLv2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

An Ansible collection to install, configure, and manage [IBM Open Liberty](https://openliberty.io/) application server on Linux hosts. Supports **Core Profile**, **Web Profile**, and **Platform** (Full Platform / Jakarta EE) editions in standalone mode.

## Features

- Install Open Liberty from Maven Central archives (ZIP)
- Create a dedicated system user and group
- Manage the server lifecycle via systemd
- Render and deploy `server.xml` from a Jinja2 template
- **Deploy WAR / EAR / JAR applications** via dropins or explicit `server.xml` entries
- **In-place version upgrades** with automatic backup and version-skip detection
- **Reconfigure HTTP / HTTPS listener ports** and optionally update firewall rules
- Validate that the server started correctly and is accepting requests
- Full uninstall workflow that cleanly removes all traces

## Supported Platforms

| OS Family | Tested On |
|:----------|:----------|
| Red Hat | RHEL 8, RHEL 9, RHEL 10 |
| Debian | Ubuntu (OpenJDK + ufw support) |

## Open Liberty Editions

Open Liberty is available in several editions. For a full description of each edition see the
[Open Liberty Editions](https://github.com/ansible-middleware/open-liberty#open-liberty-editions) reference.

| Edition variable value | Description |
|:-----------------------|:------------|
| `kernel` | Minimal kernel; add features yourself |
| `webProfile` | Jakarta EE Web Profile 10 |
| `jakartaee` | Jakarta EE Platform 10 (Full Platform) |
| `microProfile` | MicroProfile 6 |

Set `openliberty_edition` to one of the above values.

## Roles

| Role | Description | README |
|:-----|:------------|:-------|
| [`install`](roles/install/) | Download, verify, and extract Open Liberty | [README](roles/install/README.md) |
| [`server_config`](roles/server_config/) | Render `server.xml`, `jvm.options`, and `bootstrap.properties` | [README](roles/server_config/README.md) |
| [`systemd`](roles/systemd/) | Create and enable the systemd service unit | [README](roles/systemd/README.md) |
| [`app_deploy`](roles/app_deploy/) | Deploy WAR/EAR/JAR applications (dropins or explicit entries) | [README](roles/app_deploy/README.md) |
| [`version_update`](roles/version_update/) | In-place upgrade to a new Open Liberty version with backup | [README](roles/version_update/README.md) |
| [`port_config`](roles/port_config/) | Reconfigure HTTP/HTTPS listener ports and firewall rules | [README](roles/port_config/README.md) |
| [`validation`](roles/validation/) | Health check: service status + port wait + optional `/health` endpoint | [README](roles/validation/README.md) |
| [`uninstall`](roles/uninstall/) | Stop service, remove files, remove user/group | [README](roles/uninstall/README.md) |

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Java 17+ on target hosts (the role will optionally install it)
- `unzip` on target hosts (installed automatically)

### Collection dependencies

```bash
ansible-galaxy collection install -r requirements.yml
```

```yaml
# requirements.yml
collections:
  - name: community.general
    version: ">=6.0.0"
  - name: ansible.posix
    version: ">=1.4.0"
```

## Quick Start

```bash
ansible-galaxy collection install middleware_automation.open_liberty
```

### Minimal inventory

```ini
[liberty_servers]
server1.example.com
server2.example.com
```

### Full installation playbook

```yaml
---
- name: Install Open Liberty – Web Profile
  hosts: liberty_servers
  vars:
    openliberty_version: "24.0.0.9"
    openliberty_edition: webProfile
    openliberty_install_java: true
  roles:
    - middleware_automation.open_liberty.install
    - middleware_automation.open_liberty.server_config
    - middleware_automation.open_liberty.systemd
    - middleware_automation.open_liberty.validation
```

See [`playbooks/`](playbooks/) for more examples.

## Variables Reference

All variables are documented in each role's `defaults/main.yml` and the role README.

### Core (`install` / `server_config` / `systemd`)

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_version` | Open Liberty version to install | `"24.0.0.9"` |
| `openliberty_edition` | Edition: `kernel`, `webProfile`, `jakartaee`, `microProfile` | `"webProfile"` |
| `openliberty_install_dir` | Base installation directory | `/opt/openliberty` |
| `openliberty_server_name` | Liberty server name | `defaultServer` |
| `openliberty_user` | System user to run the service | `liberty` |
| `openliberty_group` | System group | `liberty` |
| `openliberty_install_java` | Install OpenJDK when missing (`openliberty_java_version`) | `false` |
| `openliberty_java_home` | JAVA_HOME (auto-discovered when install_java is true) | `/usr/lib/jvm/java-17-openjdk` |
| `openliberty_http_port` | HTTP listener port | `9080` |
| `openliberty_https_port` | HTTPS listener port | `9443` |
| `openliberty_jvm_options` | Extra JVM options written to `jvm.options` | `[]` |

### Application Deployment (`app_deploy`)

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_applications` | List of apps to deploy. Each item: `name`, `src`, `type` (optional), `context_root` (optional), `state` (`present`/`absent`), `checksum` (optional) | `[]` |
| `openliberty_deploy_to_dropins` | When `true`, copies archives to `dropins/` for auto-discovery | `false` |
| `openliberty_deploy_validate` | Probe the app context root after deployment | `true` |
| `openliberty_deploy_backup` | Timestamp-back up replaced archives | `true` |
| `openliberty_deploy_wait_timeout` | Seconds to wait for each app to become active | `120` |
| `openliberty_deploy_wait_delay` | Retry interval for readiness probe | `5` |

### Version Update (`version_update`)

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_new_version` | Target version to upgrade to | `"24.0.0.9"` |
| `openliberty_update_backup` | Back up the existing `wlp/` directory before replacing | `true` |
| `openliberty_download_url` | Override download URL (leave empty for Maven Central) | `""` |
| `openliberty_download_checksum` | Optional `sha256:<hex>` checksum for the new archive | `""` |

### Port Configuration (`port_config`)

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_http_port` | HTTP listener port (set to `-1` to disable) | `9080` |
| `openliberty_https_port` | HTTPS listener port (set to `-1` to disable) | `9443` |
| `openliberty_https_enabled` | Enable the HTTPS listener (requires SSL/keystore for production) | `false` |
| `openliberty_endpoint_host` | Network interface to bind (`*` = all) | `"*"` |
| `openliberty_endpoint_id` | `<httpEndpoint>` element ID in `server.xml` | `defaultHttpEndpoint` |
| `openliberty_http_max_keep_alive_requests` | Max persistent requests per connection | `100` |
| `openliberty_http_persist_timeout` | Keep-alive timeout in seconds | `30` |
| `openliberty_firewall_port_manage` | Open ports in firewalld/ufw | `false` |
| `openliberty_firewall_zone` | firewalld zone for port rules | `public` |

### Validation (`validation`)

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_validate_health_endpoint` | Perform HTTP health check | `true` |
| `openliberty_health_url_path` | URL path to query (requires `mpHealth` feature) | `"/health"` |
| `openliberty_validation_timeout` | Total seconds to wait for the server | `300` |
| `openliberty_validation_delay` | Seconds between retry attempts | `10` |

### Uninstall (`uninstall`)

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_remove_user` | Remove the `liberty` system user | `true` |
| `openliberty_remove_group` | Remove the `liberty` system group | `true` |

## Playbooks

| Playbook | Description |
|:---------|:------------|
| [`install.yml`](playbooks/install.yml) | Install Open Liberty and bring the server online |
| [`install_jakartaee.yml`](playbooks/install_jakartaee.yml) | Install Jakarta EE Full Platform edition |
| [`install_microprofile.yml`](playbooks/install_microprofile.yml) | Install MicroProfile edition |
| [`deploy_app.yml`](playbooks/deploy_app.yml) | Deploy WAR/EAR/JAR applications |
| [`version_update.yml`](playbooks/version_update.yml) | In-place upgrade to a new version |
| [`port_config.yml`](playbooks/port_config.yml) | Reconfigure HTTP/HTTPS listener ports |
| [`upgrade.yml`](playbooks/upgrade.yml) | Rolling upgrade (stop → install → reconfigure → restart) |
| [`validate.yml`](playbooks/validate.yml) | Run the validation role against live hosts |
| [`uninstall.yml`](playbooks/uninstall.yml) | Cleanly remove Open Liberty from hosts |

## Molecule Test Scenarios

CI runs `default` and `microprofile`. The other scenarios are for local runs.

| Scenario | CI | Roles exercised | Description |
|:---------|:---|:----------------|:------------|
| [`default`](molecule/default/) | yes | install, server_config, systemd | webProfile on RHEL 8/9/10; service active; idempotence |
| [`microprofile`](molecule/microprofile/) | yes | install, server_config, systemd, validation | MicroProfile; `/health` returns 200 |
| [`app_deploy`](molecule/app_deploy/) | local | app_deploy | WAR via configDropins and dropins; backup; ownership |
| [`port_config`](molecule/port_config/) | local | port_config | Port reconfiguration 9080→8080; old port closed |
| [`version_update`](molecule/version_update/) | local | version_update | Upgrade 24.0.0.9→24.0.0.12; backup dir; downgrade refused |
| [`validation`](molecule/validation/) | local | validation | Service check, port wait, `/health` |
| [`uninstall`](molecule/uninstall/) | local | uninstall | Install dir, unit, user, group, and port removed |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
