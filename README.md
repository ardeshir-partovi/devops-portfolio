# DevOps Portfolio Demo

A lightweight containerized HTTP service demonstrating
cross-architecture deployments on ARM64 and AMD64.

## Features

- Python HTTP service
- JSON responses
- Health endpoint at `/health`
- Docker image built on each target architecture
- Non-root container user
- Docker health check
- Localhost-only port bindings for initial testing

## Run locally

Build the image:

```bash
docker build -t portfolio-demo:1.0.0 .
```

Run the container:

```bash
docker run -d --name portfolio-demo \
  -p 127.0.0.1:8081:8080 portfolio-demo:1.0.0
```

Test the endpoints:

```bash
curl http://127.0.0.1:8081/
curl http://127.0.0.1:8081/health
```

## Architecture

The same source code is built independently on ARM64 and AMD64.
The `/` endpoint reports the running architecture, while `/health`
provides a basic health check.

## Planned improvements

- Automated tests
- GitHub Actions CI
- Automated deployment using Ansible
- Monitoring and alerting
- Deployment rollback documentation
