package main

import (
	"log"
	"math/rand/v2"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type metrics struct {
	cpuTemp    prometheus.Gauge
	hdFailures *prometheus.CounterVec
}

func NewMetrics(reg prometheus.Registerer) *metrics {
	m := &metrics{
		cpuTemp: prometheus.NewGauge(prometheus.GaugeOpts{
			Name: "cpu_temperature_celsius",
			Help: "Current temperature of the CPU.",
		}),
		hdFailures: prometheus.NewCounterVec(
			prometheus.CounterOpts{
				Name: "hd_errors_total",
				Help: "Number of hard-disk errors.",
			},
			[]string{"device"},
		),
	}
	reg.MustRegister(m.cpuTemp)
	reg.MustRegister(m.hdFailures)
	return m
}

func main() {
	// Create a non-global registry.
	reg := prometheus.NewRegistry()

	// Create new metrics and register them using the custom registry.
	m := NewMetrics(reg)

	go func() {
		for {
			// Set values for the new created metrics.
			m.cpuTemp.Set(rand.Float64() * 10)
			m.hdFailures.With(prometheus.Labels{"device": "/dev/sda"}).Inc()
			time.Sleep(time.Second * 1)
		}
	}()

	// Expose metrics and custom registry via an HTTP server
	// using the HandleFor function. "/metrics" is the usual endpoint for that.
	http.Handle("/metrics", promhttp.HandlerFor(reg, promhttp.HandlerOpts{Registry: reg}))
	log.Fatal(http.ListenAndServe(":8080", nil))
}
