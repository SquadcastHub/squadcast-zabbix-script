#!/bin/bash

url="$1"		

subject="$2"
message="$3"

curl --header "Content-Type: application/json" \
  --request POST \
  --data "${message}" \
  $url
