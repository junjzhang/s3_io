#!/bin/bash

set -e

# set up environment
unset http_proxy
unset https_proxy
source ./scripts/set_up_env.sh

pixi r download_internvid_to_s3