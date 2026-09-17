# Create a cluster with kind of the name "devops-lab" with kubernetes version v1.37.0
resource "kind_cluster" "devops" {
    name = "devops-lab"
    node_image = "kindest/node:v1.37.0@sha256:a1ed56cfb0e7b93589bdf97c8cd566405a265939e3620fc4f5de89adff580ae5"
    wait_for_ready = true
    kubeconfig_path = "${path.module}/kubeconfig"
}
