export FSSPEC_S3_ENDPOINT_URL="http://minio.minio-tenant.svc.cluster.local"
export FSSPEC_S3_KEY=""
export FSSPEC_S3_SECRET=""
export AWS_ENDPOINT_URL="$FSSPEC_S3_ENDPOINT_URL"
export AWS_ACCESS_KEY_ID="$FSSPEC_S3_KEY"
export AWS_SECRET_ACCESS_KEY="$FSSPEC_S3_SECRET"
export AWS_ALLOW_HTTP=true
export AWS_REGION="us-west-1"
export AWS_CONDITIONAL_PUT="etag"