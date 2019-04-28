Docker Usage:
```
docker run -dit --name ick nsuave/ick
docker exec -d ick python3 /ick/ick.py $baseDomain $series $type $key $domain $address
```

Python Usage:
```
python3 ick.py $baseDomain $series $type $key $domain $address
```