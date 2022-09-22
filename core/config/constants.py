# whiterose
TIMEZONES = {
    "MX": "Mexico/General"
}

TRACE_STDOUT = True

# Webhhok
HOOK_POST = True
HOOK_URL = "https://hooks.slack.com/services/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"
HOOK_OK = "Operation Successful"
HOOK_ERR = "System Failure"

# logs
LOG_LEVEL = "info"
LOG_URL = "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logs:"

# HTTP Request
HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']
HTTP_CONTENT_TYPE = 'application/json'
CORS_HEADERS = ['Content-Type',
                'X-Amz-Date',
                'Authorization',
                'X-Api-Key',
                'x-requested-with']
CORS_ORIGINS = '*'
CORS_X_REQUEST = '*'

