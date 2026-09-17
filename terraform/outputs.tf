output "cluster_name" {
  value = kind_cluster.devops.name
}

output "kubeconfig_path" {
  value = kind_cluster.devops.kubeconfig_path
}