# Monitoring for Visual Analytics Tool
Prometheus values can be found at https://github.com/prometheus-community/helm-charts/blob/main/charts/prometheus/values.yaml

## Logging Setup
helm repo add grafana https://grafana.github.io/helm-charts
helm pull grafana/loki

Values in https://github.com/grafana/loki/tree/main/production/helm/loki

we deploy it in SingleBinary mode since our log volume is not that large