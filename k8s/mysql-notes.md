# MySQL in Kubernetes
Choose the database target before deploying the backend:
1. Recommended learning path on AWS: Amazon RDS MySQL with restricted network access.
2. Disposable local cluster: a StatefulSet and PersistentVolumeClaim.

Do not run MySQL as a stateless Deployment or rely on container filesystem storage. Set DB_HOST to a reachable database endpoint and create the Kubernetes Secret securely.
