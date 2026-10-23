# AGENTS.md

Agent guidance for the `basic_service` Ansible role lives in `.cursor/rules/cursor-cloud.mdc`.

```bash
yamllint --config-file ./tests/yaml-lint.yml .
ansible-lint --config-file ./tests/ansible-lint.yml .
helm lint helm
helm template basic-service-ci helm -f helm/values.yaml >/dev/null
helm template basic-service-ci helm -f helm/values-test.yaml >/dev/null
helm template basic-service-ci helm -f tests/fixtures/k8s-rendered-values.yaml >/dev/null
for scenario in \
  systemd-basic \
  systemd-full \
  systemd-uninstall \
  container-basic \
  container-binary \
  container-binary-service \
  container-full \
  container-hostnet \
  container-uninstall \
  install-basic \
  install-uninstall \
  k8s-basic; do
  (cd tests && molecule test -s "$scenario")
done
```
