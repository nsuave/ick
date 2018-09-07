Usage:
```
docker build -t nsuave/imgchap .
docker run --name imgchap -dt nsuave/imgchap
docker exec -d imgchap /imgchap/imgchap.sh
docker cp imgchap:/path/to/files .
```