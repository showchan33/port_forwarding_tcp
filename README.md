# port_forwarding_tcp
 
Shell script to realize port forwarding in tcp communication.

# Requirement

* OS
    * Linux (amd64, arm64)
* Tools
    * sh
    * iptables
    * Docker, Docker Compose (Necessary if you want to run sample)

# Usage

Set the following environment variables.

| Environment Variable | Description |
| --- | --- |
| CHAIN | Name of the chain used by iptables |
| SRC_PORT | Destination port number **before** NAT |
| DST_IP | Destination IP address **after** NAT |
| DST_PORT | Destination port number **after** NAT |
| DELETE | Set to "true" to delete the setting<br> |

Then, run ``port_forwarding_tcp.sh``.

# Example

Make the web server at 93.184.216.34 (same as example.com) accessible from localhost on port 10443.

```
sudo \
CHAIN=MYCHAIN \
SRC_PORT=10443 \
DST_IP=93.184.216.34 \
DST_PORT=443 \
./port_forwarding_tcp.sh
```

Make sure you can access it on localhost port 10443.

```
curl -ik https://localhost:10443
```

Delete the port forwarding setting.

```
sudo \
DELETE=true \
CHAIN=MYCHAIN \
SRC_PORT=10443 \
DST_IP=93.184.216.34 \
DST_PORT=443 \
./port_forwarding_tcp.sh
```

# Sample with docker compose


You can also check the operation with docker compose.

```
docker compose up
```

# Author
 
showchan33

# License
"port_forwarding_tcp" is under [GPL license](https://www.gnu.org/licenses/licenses.en.html).
