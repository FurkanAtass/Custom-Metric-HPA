# Kubernetes AI Inference Scaling with Custom Metrics

This project demonstrates a robust setup for dynamically scaling an AI inference service on Kubernetes, using custom metrics to ensure optimal performance and resource efficiency. It leverages Minikube for local deployment, Prometheus for monitoring, and a custom metrics-driven Horizontal Pod Autoscaler (HPA) to adjust pod counts based on real-time inference load.

This setup dynamically scales the Kubernetes cluster by monitoring the average inference time, ensuring optimal availability and performance. 

## Getting Started

### Prerequisites

- Docker
- Kubernetes CLI (kubectl)
- Minikube
- Helm

### Initial Setup

1. **Start Minikube**: Initialize a Minikube cluster with the desired configuration to simulate a Kubernetes environment locally.
 Use the -n option to set the number of nodes and --memory to allocate RAM in MB.

```shell
minikube start -n 2 --memory 4400
```

2. **Enable Metrics Server**: Activate Minikube's metrics server to collect and analyze metrics for Kubernetes objects, which is crucial for the HPA.

```shell
minikube addons enable metrics-server
```

## Application Deployment

The application is a Python-based AI inference service designed for high efficiency and scalability. It simulates a 10 seconds inference time application.

### Application Details

- HTTP Keep-Alive: Utilizes persistent TCP connections to ensure long-lived interactions with clients, optimizing connection overhead and latency. **Ensures even load distribution**. 
- ThreadPoolExecutor: Enhances endpoint responsiveness and accuracy of metric calculations, critical for effective scaling decisions. **Keeps the */metrics* endpoint responsive during inference operations**.

### Deploying to Kubernetes

Deploy the application and its services to Kubernetes using the provided ***deployment.yaml*** and ***service.yaml*** files.

```shell
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Prometheus Integration

Prometheus is set up to monitor custom metrics from the **/metrics** endpoint of the AI inference service, allowing for detailed insight into performance and workload.

### Setup Prometheus:

```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -f prometheus-values.yaml
```
***prometheus-values.yaml*** file determines the scraping configurations for Prometheus.

### Access Prometheus UI:

To see the Prometheus dashbord on a web browser:
```shell
kubectl port-forward service/prometheus-kube-prometheus-prometheus 9090
```

Then, visit [http://localhost:9090/](http://localhost:9090/) to view the Prometheus dashboard.

## Prometheus Adapter

The ***prometheus-adapter.yaml*** file is crucial for converting Prometheus metrics into a format Kubernetes can use, specifically for scaling decisions by the HPA based on custom metrics. 
```shell
helm install prometheus-adapter prometheus-community/prometheus-adapter -f prometheus-adapter.yaml
```
In the ***prometheus-adapter.yaml***, the metricsQuery section allows you to define custom queries to tailor the metrics to your application's specific needs. To create effective queries, explore Prometheus's query language and test your queries directly in the Prometheus dashboard. This process helps you design queries that accurately reflect your application's performance and scaling requirements.
## Observing Metrics

Custom metrics derived from Prometheus can be observed and tested for accuracy and relevance, ensuring the HPA makes informed scaling decisions.

### View Custom Metrics:

```shell
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1/namespaces/default/python_request_duration_seconds_per_request" | jq .
```

or you can use the **metricsQuery** in the ***prometheus-adapter.yaml*** on Prometheus dashboard. 
## HPA with Custom Metrics

The ***hpa.yaml*** file configures the HPA to scale the application based on custom metrics, with behavior adjustments to accommodate the high inference times of AI workloads.
```shell
kubectl apply -f hpa.yaml
```
The behavior section in the HPA configuration is strategically designed to introduce stability during autoscaling by managing the pace of scale-up and scale-down actions. With a stabilizationWindowSeconds set for both scaling up (240 seconds) and down (300 seconds), it ensures that scaling decisions are moderated over these time frames, preventing rapid fluctuations in pod count.
## Conclusion

This project provides a scalable, efficient solution for deploying AI inference services on Kubernetes, leveraging the power of custom metrics for intelligent scaling. By integrating Prometheus and the Prometheus Adapter, it offers deep insights into application performance, ensuring resources are optimally utilized to meet demand.