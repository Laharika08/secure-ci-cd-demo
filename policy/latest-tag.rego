package main

"""
Policy: latest-tag.rego

This OPA policy denies Kubernetes Deployments that specify container images
ending with the literal tag `:latest`.  Using the `latest` tag is considered
bad practice because it makes deployments non‑deterministic and can lead to
unexpected changes when new image versions are pushed.  Instead, specify an
immutable version tag for all containers.

Conftest searches for `deny` rules in the `main` package; any messages
returned cause a failure during `conftest test`.
"""

deny[msg] {
  # Ensure the resource is a Deployment
  input.kind == "Deployment"
  # Iterate over each container in the pod spec
  container := input.spec.template.spec.containers[_]
  # Check if the image name ends with ':latest'
  endswith(container.image, ":latest")
  msg := sprintf("Container image '%s' uses the disallowed 'latest' tag.", [container.image])
}
