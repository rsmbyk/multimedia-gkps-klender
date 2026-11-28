# Quickstart — spec 255

See [`data-model.md`](./data-model.md) for the record and [`contracts/none.md`](./contracts/none.md)
for the (absent) external interface.

## Local run

```
cd ~/Projects/multimedia-gkps-klender-255
python3 run-tests.py tests.e2e.test_use_template_progress_persist tests.e2e.test_use_template_progress tests.e2e.test_tatib_templates --keepdb --noinput
```

`run-tests.py` is a machine-local helper that reads the compose credential at runtime; it is not part
of the repository.

## Preview

```
cd specs/255-use-template-progress-persist/preview
python3 build_preview.py
../../../../multimedia-gkps-klender/.venv/bin/python probe.py
```

The page opens the three indicator variants; variant A is the chosen one. The probe measures both
states and writes `shots/indicators.png`.