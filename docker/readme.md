# Prometheus
## doc
* https://prometheus.io/docs/prometheus/latest/getting_started/
## run
* docker run -p 9090:9090 -v ~/prometheus/prometheus.yaml:/etc/prometheus/prometheus.yaml prom/prometheus

# Grafana
## doc
* https://grafana.com/docs/grafana/latest/
## run
* docker run -p 3000:3000 --name=grafana grafana/grafana-enterprise
* user/pass: admin/admin