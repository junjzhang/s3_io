#!/bin/bash

set -e

# set up environment
unset http_proxy
unset https_proxy
source ./scripts/set_up_env.sh

pixi r process_and_upload_to_s3