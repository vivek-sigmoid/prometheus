from kubernetes import client, config
from time import sleep
from prometheus_client import Gauge, start_http_server
from http.server import BaseHTTPRequestHandler

config.load_kube_config()
api = client.CustomObjectsApi()


class CustomCollector(BaseHTTPRequestHandler):
    def collect(self):
        pod_resource = api.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1",
                                                         namespace="default",
                                                         plural="pods")
        ram_metrics_pod_usage_info = Gauge("pod_usage_info_memory", "Memory usage in bytes p1.",
                                           {'host': 'pod_usage_info'})
        cpu_metrics_pod_usage_info = Gauge("pod_usage_info_cpu", "CPU usage details p1", {'host': 'pod_usage_info'})
        ram_metrics_usage_info = Gauge("usage_info_memory", "Memory usage in bytes p2",
                                       {'host': 'pod_usage_info'})
        cpu_metrics_usage_info = Gauge("usage_info_cpu", "CPU usage details p2", {'host': 'pod_usage_info'})
        pod_counter = Gauge("count_no_of_pods", "no of pods deployed")
        for pod in pod_resource["items"]:
            for details in pod['containers']:
                print(details.get('name'))

        while True:
            pod_resource = api.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1",
                                                             namespace="default",
                                                             plural="pods")
            list = []
            for pod in pod_resource["items"]:
                for details in pod['containers']:
                    list.append(details.get('usage'))
            mem = list[0].get('memory')[:-2]
            ram_metrics_pod_usage_info.labels('ram_used').set(mem)
            cpu = list[0].get('cpu')[:-1]
            cpu_metrics_pod_usage_info.labels('cpu_usage').set(cpu)
            mem = list[1].get('memory')[:-2]
            ram_metrics_usage_info.labels('ram_used').set(mem)
            cpu = list[1].get('cpu')[:-1]
            cpu_metrics_usage_info.labels('cpu_usage').set(cpu)
            pod_counter.set(len(list))
            sleep(3)


if __name__ == "__main__":
    try:
        start_http_server(3333)
        x = CustomCollector
        x.collect(self=x)
    except KeyboardInterrupt:
        exit(0)
