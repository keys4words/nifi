token=$(curl -d 'username=admin&password=superpupersecret' -H 'Content-Type: application/x-www-form-urlencoded' -X POST https://localhost:8444/nifi-api/access/token --insecure)
curl -H 'Content-Type: application/x-www-form-urlencoded' -H "Authorization: Bearer $token" -X GET https://localhost:8444/nifi-api/access/token/expiration --insecure
curl -H 'Content-Type: application/x-www-form-urlencoded' -H "Authorization: Bearer $token" -X GET https://localhost:8444/nifi-api/controller/cluster --insecure