Usage:
```
docker run --name imgchap --mount type=bind,source="$(pwd)"/chapters,target=/tmp -dt nsuave/imgchap
docker exec -d imgchap /imgchap/imgchap.sh
```