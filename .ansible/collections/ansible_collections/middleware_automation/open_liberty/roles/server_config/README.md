# middleware_automation.open_liberty.server_config

Create a Liberty server instance and render its configuration files
(`server.xml`, `jvm.options`, `bootstrap.properties`) from Jinja2 templates.

## Requirements

- Ansible >= 2.16
- Python >= 3.12 on the Ansible controller
- Open Liberty installed by the [`install`](../install/README.md) role
- `become: true` (root privileges)

## Role Variables

### Server identity

| Variable | Default | Description |
|---|---|---|
| `openliberty_server_name` | `defaultServer` | Liberty server instance name |
| `openliberty_edition` | `webProfile` | Edition — drives default feature set in `server.xml` |
| `openliberty_server_create` | `true` | Run `server create` if the instance directory is absent |
| `openliberty_server_description` | `"Open Liberty Server managed by Ansible"` | Free-text description written into `server.xml` |

### Paths and ownership

| Variable | Default | Description |
|---|---|---|
| `openliberty_home` | `/opt/openliberty/wlp` | Liberty home directory (must match `install` role) |
| `openliberty_user` | `liberty` | Owner of all generated files |
| `openliberty_group` | `liberty` | Group of all generated files |

### HTTP listener

| Variable | Default | Description |
|---|---|---|
| `openliberty_http_port` | `9080` | HTTP listener port |
| `openliberty_https_port` | `9443` | HTTPS listener port |
| `openliberty_https_enabled` | `true` | Enable the HTTPS listener in `server.xml` |

### Features

| Variable | Default | Description |
|---|---|---|
| `openliberty_extra_features` | `[]` | Additional feature names appended beyond edition defaults. Example: `["jdbc-4.3", "jndi-1.0"]` |

### Data sources

| Variable | Default | Description |
|---|---|---|
| `openliberty_datasources` | `[]` | List of `<dataSource>` stanzas rendered into `server.xml`. Each item: `id`, `jdbcDriverRef`, `databaseName` (or `url`), `user`, `password` |

### JVM options

| Variable | Default | Description |
|---|---|---|
| `openliberty_jvm_options` | `[]` | JVM options written to `jvm.options`, e.g. `["-Xms512m", "-Xmx1024m"]` |

### Bootstrap properties

| Variable | Default | Description |
|---|---|---|
| `openliberty_bootstrap_properties` | `{}` | Key-value pairs written to `bootstrap.properties`. Example: `{"com.ibm.ws.logging.trace.specification": "*=all=enabled"}` |

### Logging

| Variable | Default | Description |
|---|---|---|
| `openliberty_configure_logging` | `true` | Add a `<logging>` stanza to `server.xml` |
| `openliberty_log_level` | `"INFO"` | Log level: `INFO`, `AUDIT`, `WARNING`, `ERROR` |
| `openliberty_log_max_file_size` | `20` | Maximum log file size in MB (0 = unlimited) |
| `openliberty_log_max_files` | `5` | Maximum number of log files to retain (0 = unlimited) |
| `openliberty_log_dir` | `""` | Custom log directory (empty = Liberty default) |

## Dependencies

[`middleware_automation.open_liberty.install`](../install/README.md)

## Example Playbook

```yaml
- name: Configure Open Liberty server
  hosts: liberty_servers
  vars:
    openliberty_server_name: prodServer
    openliberty_http_port: 8080
    openliberty_https_enabled: false
    openliberty_extra_features:
      - jdbc-4.3
      - jndi-1.0
    openliberty_jvm_options:
      - "-Xms256m"
      - "-Xmx512m"
    openliberty_datasources:
      - id: appDB
        jdbcDriverRef: PostgreSQL
        url: "jdbc:postgresql://db.internal:5432/app"
        user: appuser
        password: "{{ vault_db_password }}"
  roles:
    - role: middleware_automation.open_liberty.install
    - role: middleware_automation.open_liberty.server_config
```

## Molecule Tests

| Scenario | What is tested |
|---|---|
| [`default`](../../molecule/default/) | webProfile `server.xml` on RHEL 8, 9, and 10 |
| [`microprofile`](../../molecule/microprofile/) | MicroProfile edition configuration |
| [`app_deploy`](../../molecule/app_deploy/) | Configuration before deployment |
| [`port_config`](../../molecule/port_config/) | Configuration before port reconfiguration |
| [`version_update`](../../molecule/version_update/) | Configuration before version upgrade |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
