#bin/bash
sudo rm -f $2
sudo $1/firecracker --api-sock $2
