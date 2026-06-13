# 🚀 Production-Ready DevOps Sandbox eCommerce App

A sleek, lightweight, database-free Python Flask web application designed specifically to practice DevOps engineering workflows like Dockerization, Continuous Integration (CI), Continuous Deployment (CD), and cloud orchestration.

## 🛠️ Features for DevOps Practice
- **Stateless Architecture**: Shopping carts are persisted using signed browser cookies (`flask.session`). No state is stored on disk or database, making this application perfect for practicing zero-downtime horizontal scaling.
- **Configurable Context**: Detects and prints environment variables dynamically (e.g., `APP_ENV`) to test ConfigMaps or custom environment injection.
- **Health Check Endpoint**: Includes a structured JSON `/health` route, perfect for configuring Kubernetes Readiness/Liveness Probes or AWS Target Group monitoring.
- **Production Server Ready**: Packaged with `gunicorn` to practice migrating from Flask's built-in development server to an industrial WSGI engine.

---

## 🏃 Local Development Quickstart

1. **Clone & Enter directory:**
   ```bash
   git clone <your-repo-url>
   cd flask-devops-ecommerce