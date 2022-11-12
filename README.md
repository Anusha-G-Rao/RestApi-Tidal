## RestApi-Tidal

######  Request 
```
GET /
```
```
curl -i -H 'Accept: application/json' http://localhost:8080/
```
######  Response:
```
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.8.10
Date: Sat, 12 Nov 2022 18:37:53 GMT
Content-Type: application/json
Content-Length: 32
Connection: close

{"message":"You have arrived!"}
```

######  Request
```
GET /healthcheck
```
```
curl -i -H 'Accept: application/json' http://localhost:8080/healthcheck
```
######  Response:
```
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.8.10
Date: Sat, 12 Nov 2022 18:39:25 GMT
Content-Type: application/json
Content-Length: 26
Connection: close

{"message":"Good Health"}
```

######  Request
```
POST /register
```
```
curl -i -X POST -H "Content-Type: application/json" -d '{"password": "nailit", "email": "brandon@example.com"}' http://localhost:8080/register
```
######  Response
```
HTTP/1.1 201 CREATED
Server: Werkzeug/2.2.2 Python/3.8.10
Date: Sat, 12 Nov 2022 18:49:26 GMT
Content-Type: application/json
Content-Length: 40
Connection: close

{"message":"User created successfully"}
```

######  Request
```
POST /login
```
```
curl -i -X POST -H "Content-Type: application/json" -d '{"password": "nailit", "email": "brandon@example.com"}' http://localhost:8080/login
```
######  Response
```
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.8.10
Date: Sat, 12 Nov 2022 18:51:00 GMT
Content-Type: application/json
Content-Length: 337
Connection: close
{"access_token":"***Assess Token***","message":"login succeeded!"}
```

######  Request
```
POST /block
```
```
curl -i -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"cidr":"172.19.0.0/24","ttl":"60"}' http://172.19.0.1:8080/block
```
######  Reponse
```
HTTP/1.1 201 CREATED
Server: Werkzeug/2.2.2 Python/3.8.10
Date: Sat, 12 Nov 2022 18:56:37 GMT
Content-Type: application/json
Content-Length: 58
Connection: close

{"message":"Requests will be blocked from an IP in CIDR"}
```
######  Testing:
All endpoints except the default '/' will be blocked for the IPs iin the CIDR block range.
```
curl -i -H 'Accept: application/json' http://localhost:8080/healthcheck
```
######  Response
```
HTTP/1.1 403 FORBIDDEN
Server: Werkzeug/2.2.2 Python/3.8.10
Date: Sat, 12 Nov 2022 18:56:44 GMT
Content-Type: application/json
Content-Length: 37
Connection: close

{"Message":"Cannot process request"}
```

######  Request
```
GET /stats
```
```
curl -i -H 'Accept: application/json' http://localhost:8080/stats
```
######  Response
```
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.8.10
Date: Sat, 12 Nov 2022 19:01:35 GMT
Content-Type: application/json
Content-Length: 296
Connection: close

{"accepted_request":8,"blocked_request":2,"cidr":[{"cidr":"172.19.0.0/24","currentts":"2022-11-12T18:55:11.672251","expirets":"2022-11-12T18:56:11.672234","id":1,"ttl":60},{"cidr":"172.19.0.0/24","currentts":"2022-11-12T18:56:37.956956","expirets":"2022-11-12T18:57:37.956935","id":2,"ttl":60}]}
```

Future Improvements:

Change the password from plain text to hash.
Testing his on AWS creating a VPC and subnets.
Rate limiter
