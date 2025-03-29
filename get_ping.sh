#!/bin/sh

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <destination_ip>"
    exit 1
fi

# Get destination IP from argument
dst_ip="$1"

# Execute ping once to the specified IP
ping_result=$(ping -c 1 ${dst_ip} | grep "time=" | sed 's/.*time=\([0-9.]*\).*/\1/')

# Output in JSON format
echo "{'dst':'${dst_ip}','response_ms':${ping_result}}"
 