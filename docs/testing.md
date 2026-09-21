# Testing

## Continuous integration

The collection is tested with a [molecule](https://github.com/ansible-community/molecule) setup covering the included roles and verifying correct installation and idempotency.
In order to run the molecule tests locally with Python 3.12 available, after cloning the repository:

```
pip install yamllint 'molecule[docker]~=3.5.2' ansible-core flake8 ansible-lint voluptuous
molecule test --all
```

## Test playbooks

Sample playbooks are provided in the `playbooks/` directory; to run the playbooks locally (requires a RHEL system with Python 3.12+, ansible, and systemd) the steps are as follows:

```
# setup environment
pip install ansible-core
# clone the repository
git clone https://github.com/ansible-middleware/open-liberty
cd open-liberty
# install collection dependencies
ansible-galaxy collection install -r requirements.yml
# create inventory for localhost
cat << EOF > inventory
[liberty_servers]
localhost ansible_connection=local
EOF
# run a playbook
ansible-playbook -i inventory playbooks/install.yml
```
