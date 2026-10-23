# AGENTS.md

Agent guidance for the `basic_service` Ansible role lives in `.cursor/rules/cursor-cloud.mdc`.

```bash
yamllint --config-file ./tests/yaml-lint.yml .
helm lint helm
helm template basic-service-ci helm -f helm/values.yaml >/dev/null
helm template basic-service-ci helm -f helm/values-test.yaml >/dev/null
helm template basic-service-ci helm -f tests/fixtures/k8s-rendered-values.yaml >/dev/null
cd tests && molecule test -s container-basic
```
