# Create a cluster with kind of the name "devops-lab" with kubernetes version v1.37.0
resource "kind_cluster" "devops" {
  name            = "devops-lab"
  node_image      = "kindest/node:v1.34.3@sha256:08497ee19eace7b4b5348db5c6a1591d7752b164530a36f855cb0f2bdcbadd48"
  wait_for_ready  = true
  kubeconfig_path = "${path.module}/kubeconfig"
}


