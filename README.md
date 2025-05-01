# Event-Driven Kubernetes Deployment with Private Registry

This project implements an **event-driven continuous deployment system** for Kubernetes using a private Docker registry, Knative Eventing, and automated deployment updates. Whenever a new Docker image is pushed, the corresponding Kubernetes deployment is updated automatically.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Key Components](#key-components)
- [How It Works](#how-it-works)
- [File Structure](#file-structure)
- [Setup \& Usage](#setup--usage)

---

## Overview

This repository demonstrates a fully automated CI/CD pipeline for Kubernetes:

- **Private Registry:** Hosts Docker images for your applications.
- **Knative Eventing:** Captures image push events and triggers deployment updates.
- **Registry Monitor:** Watches for new image tags and updates deployments.
- **Automated Rollout:** Deployments are updated in real time when new images are available.

---

## Architecture

The system consists of the following workflow:

1. **Image Build \& Push:** Developers push new images (e.g., `my-webapp:v5`) to the private registry.
2. **Event Emission:** The registry emits a webhook event on each image push.
3. **Event Capture:** Knative Eventing (via `WebhookSource` and `Trigger`) captures the event and forwards it to the deployment updater service.
4. **Deployment Update:** The updater service or registry monitor updates the Kubernetes deployment with the new image tag.

---

## Key Components

| Component | Description |
| :-- | :-- |
| **my-webapp** | Flask-based web app, containerized and deployed via Kubernetes. |
| **registry-monitor** | Python service that polls the registry for new image tags and updates the deployment using `kubectl`. |
| **Knative Eventing** | Handles event flow from Docker image push to deployment update. |
| **updater-service** | Knative Service that receives events and triggers deployment updates. |
| **Private Registry** | Stores Docker images, accessible within the cluster. |


---

## How It Works

### 1. Registry Monitor

- **Script:** [`registry-monitor/monitor.py`](./registry-monitor/monitor.py)
- **Function:** Polls the private registry for new tags (e.g., `v1`, `v2`, ...).
- **Action:** On detecting a new tag, updates the Kubernetes deployment using:

```bash
kubectl set image deployment/my-webapp web-container=registry.dev.svc.cluster.local:5000/my-webapp:&lt;tag&gt;
```


### 2. Knative Eventing

- **WebhookSource:** Receives webhook events when images are pushed.
- **Trigger:** Filters for `docker.image.push` events and forwards them to the updater service.
- **Updater Service:** Receives the event and performs the deployment update.


### 3. Security

- **RBAC:** Service accounts and roles ensure only authorized services can update deployments.
- **Image Pull Secrets:** All deployments use `regcred` for private registry access.

---

## File Structure

```plaintext
.
├── Dockerfile                    # Base Dockerfile for updater service
├── deployment.yaml               # Example deployment (nginx)
├── my-webapp/
│   ├── Dockerfile                # Dockerfile for Flask web app
│   └── app.py                    # Flask app code
├── my-webapp-deployment.yaml     # Kubernetes deployment and service for my-webapp
├── registry-monitor/
│   ├── Dockerfile                # Dockerfile for registry monitor
│   └── monitor.py                # Python registry monitor script
├── registry-monitor-deployment.yaml # Deployment, RBAC for registry monitor
├── requirements.txt              # Python dependencies
├── trigger.yaml                  # Knative eventing trigger
├── updater-service.yaml          # Knative service for deployment updater
└── webhook-source.yaml           # Knative webhook source for Docker push events
```


---

## Setup \& Usage

1. **Build and Push Images:**
Build your app and monitor images, push them to your private registry.
2. **Deploy Components:**
Apply the YAML files to your Kubernetes cluster:

```bash
kubectl apply -f my-webapp-deployment.yaml
kubectl apply -f registry-monitor-deployment.yaml
kubectl apply -f updater-service.yaml
kubectl apply -f webhook-source.yaml
kubectl apply -f trigger.yaml
```

3. **Configure Webhook:**
Set up your registry to send push events to the Knative WebhookSource endpoint.
4. **Automatic Updates:**
When a new image is pushed (e.g., `my-webapp:v5`), the deployment is updated automatically.

---

## Example: Flask Web App

The sample `my-webapp` is a simple Flask application that allows users to post messages via a web form. The service is exposed via a Kubernetes `NodePort` for easy access.

---

## Notes

- Ensure your Kubernetes nodes can resolve and access `registry.dev.svc.cluster.local:5000`.
- RBAC and imagePullSecrets are required for secure operation.
- The monitor and updater service require `kubectl` access within the cluster.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Contributions welcome!**

<div style="text-align: center">⁂</div>

[^1]: paste.txt

