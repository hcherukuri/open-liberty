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

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_server_name` | Liberty server instance name | `defaultServer` |
| `openliberty_edition` | Edition — drives default feature set in `server.xml` | `webProfile` |
| `openliberty_server_create` | Run `server create` if the instance directory is absent | `true` |
| `openliberty_server_description` | Free-text description written into `server.xml` | `"Open Liberty Server managed by Ansible"` |

### Paths and ownership

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_home` | Liberty home directory (must match `install` role) | `/opt/openliberty/wlp` |
| `openliberty_user` | Owner of all generated files | `liberty` |
| `openliberty_group` | Group of all generated files | `liberty` |

### HTTP listener

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_http_port` | HTTP listener port | `9080` |
| `openliberty_https_port` | HTTPS listener port | `9443` |
| `openliberty_https_enabled` | Enable the HTTPS listener in `server.xml` (requires SSL/keystore for production) | `false` |

### Features

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_extra_features` | Additional feature names appended beyond edition defaults. Example: `["jdbc-4.3", "jndi-1.0"]` | `[]` |

### Data sources

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_datasources` | List of `<dataSource>` stanzas rendered into `server.xml`. Each item: `id`, `jdbcDriverRef`, `databaseName` (or `url`), `user`, `password` | `[]` |

### JVM options

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_jvm_options` | JVM options written to `jvm.options`, e.g. `["-Xms512m", "-Xmx1024m"]` | `[]` |

### Bootstrap properties

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_bootstrap_properties` | Key-value pairs written to `bootstrap.properties`. Example: `{"com.ibm.ws.logging.trace.specification": "*=all=enabled"}` | `{}` |

### Logging

| Variable | Description | Default |
|:---------|:------------|:--------|
| `openliberty_configure_logging` | Add a `<logging>` stanza to `server.xml` | `true` |
| `openliberty_log_level` | Log level: `INFO`, `AUDIT`, `WARNING`, `ERROR` | `"INFO"` |
| `openliberty_log_max_file_size` | Maximum log file size in MB (0 = unlimited) | `20` |
| `openliberty_log_max_files` | Maximum number of log files to retain (0 = unlimited) | `5` |
| `openliberty_log_dir` | Custom log directory (empty = Liberty default) | `""` |

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

| Scenario | Description |
|:---------|:------------|
| [`default`](../../molecule/default/) | webProfile `server.xml` on RHEL 8, 9, and 10 |
| [`microprofile`](../../molecule/microprofile/) | MicroProfile edition configuration |
| [`app_deploy`](../../molecule/app_deploy/) | Configuration before deployment |
| [`port_config`](../../molecule/port_config/) | Configuration before port reconfiguration |
| [`version_update`](../../molecule/version_update/) | Configuration before version upgrade |

## License

GPL-2.0-only

## Author

[Harsha Cherukuri](https://github.com/hcherukuri)
