# Run backup directly

In the backup k8s namespace run:
```bash
kubectl create job --from=cronjob/backup my-test
```