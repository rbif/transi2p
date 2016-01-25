# Example

```
user@cloud1:~$ curl http://stats.i2p/ -svo /dev/null
* Hostname was NOT found in DNS cache
*   Trying 10.18.0.1...
* Connected to stats.i2p (10.18.0.1) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.38.0
> Host: stats.i2p
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Sun, 24 Jan 2016 22:58:18 GMT
< Vary: Accept-Encoding
< Accept-Ranges: bytes
< Cache-Control: max-age=3600,public
< Content-Type: text/html
< Content-Length: 13181
< Last-Modified: Thu, 22 Oct 2015 14:50:34 GMT
< Connection: close
< 
{ [data not shown]
* Closing connection 0
user@cloud1:~$ curl http://google.com/ -svo /dev/null
* Hostname was NOT found in DNS cache
*   Trying 173.194.65.113...
* Connected to google.com (173.194.65.113) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.38.0
> Host: google.com
> Accept: */*
> 
< HTTP/1.1 302 Found
< Cache-Control: private
< Content-Type: text/html; charset=UTF-8
< Location: http://www.google.cz/?gfe_rd=cr&ei=FVelVoHgOYqHOqC6o_gF
< Content-Length: 256
< Date: Sun, 24 Jan 2016 22:58:29 GMT
* Server GFE/2.0 is not blacklisted
< Server: GFE/2.0
< 
{ [data not shown]
* Connection #0 to host google.com left intact
user@cloud1:~$ curl http://3g2upl4pq6kufc4m.onion/ -svo /dev/null
* Hostname was NOT found in DNS cache
*   Trying 10.192.183.80...
* Connected to 3g2upl4pq6kufc4m.onion (10.192.183.80) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.38.0
> Host: 3g2upl4pq6kufc4m.onion
> Accept: */*
> 
< HTTP/1.1 200 OK
* Server nginx is not blacklisted
< Server: nginx
< Date: Sun, 24 Jan 2016 22:58:46 GMT
< Content-Type: text/html; charset=UTF-8
< Content-Length: 5196
< Connection: keep-alive
< ETag: "56a54bc6-144c"
< Expires: Sun, 24 Jan 2016 22:58:45 GMT
< Cache-Control: no-cache
< Accept-Ranges: bytes
< 
{ [data not shown]
* Connection #0 to host 3g2upl4pq6kufc4m.onion left intact
user@cloud1:~$ 
```

# Installation

```
pip install twisted txi2p
sudo ./rules.sh
twistd transi2p -c config.json
```

# Tor setup

```
DNSPort 5353
VirtualAddrNetworkIPv4 10.192.0.0/16
AutomapHostsOnResolve 1
TransPort 9040
```

# SAM port configuration

Go here and enable the SAM port: http://127.0.0.1:7657/configclients
