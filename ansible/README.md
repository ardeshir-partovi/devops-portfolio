# Ansible Deployment

This playbook deploys the portfolio demo to an AMD64 target.

## Prerequisites

- Ansible installed on the control node
- SSH access for the deployment user
- Docker installed on the target
- A restricted sudo rule for `/usr/local/sbin/deploy-portfolio`

## Run

Configure a private inventory and SSH key, then run:

```bash
ansible-playbook -i inventory.ini deploy.yml
```

The playbook copies the application, invokes the restricted deployment
script, and checks the HTTP health endpoint.

The deployment script is host-specific and must be installed securely
on the target before using this playbook.
