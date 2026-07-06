# AGENTS.md

Agent guidance for the `basic_service` Ansible role lives in `.cursor/rules/cursor-cloud.mdc`.

```bash
yamllint --config-file ./tests/yaml-lint.yml .
cd tests && molecule test -s container-basic
./tests/helm-validate.sh
```
