## Contributor's Guidelines

- All YAML files named with '.yml' extension
- Use spaces around jinja variables. `{{ var }}` over `{{var}}`
- Variables that are internal to the role should be lowercase and start with the role name / `openliberty_` prefix
- Keep roles self contained - Roles should avoid including tasks from other roles when possible
- Plays should do nothing more than include a list of roles except where `pre_tasks` and `post_tasks` are required when possible
- Separators - Use valid name, ie. underscores (e.g. `my_role` `my_playbook`) not dashes (`my-role`)
- Paths - When defining paths, do not include trailing slashes (e.g. `my_path: /foo` not `my_path: /foo/`). When concatenating paths, follow the same convention (e.g. `{{ my_path }}/bar` not `{{ my_path }}bar`)
- Indentation - Use 2 spaces for each indent
- `vars/` vs `defaults/` - internal or interpolated variables that don't need to change or be overridden by users go in `vars/`, those that a user would likely override, go under `defaults/` directory
- Role variable tables in README files use column order: `Variable`, `Description`, `Default`
- Prefer "Open Liberty" over bare "Liberty" in user-facing documentation
- All playbooks/roles should be focused on compatibility with Ansible Automation Platform controller

## Changelog fragments

Add a short YAML fragment under `changelogs/fragments/` for user-visible changes.
See [antsibull-changelog](https://ansible.readthedocs.io/projects/antsibull-changelog/) documentation for fragment formats.
