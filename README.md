# svrless-fw

Python lib for serverless microservices.

## API

`core.config.__init__.py`

- __def__ get_module_attr(__module(__*str*__)__, __attr(__*str*__)__)
- __def__ config_attr(__attr(__*str*__)__, __local(__*local*__)__)

`core.config.__constants__.py`

- TIMEZONES:
	+ `MX`: `Mexico/General`
- TRACE_STDOUT: (_default_: `True`)
- HOOK_POST: (_default_: `True`)
- HOOK_URL: (_default_: `https://hooks.slack.com/services/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`)
- HOOK_OK: (_default_:  `Operation Successful`)
- HOOK_ERR: (_default_: `System Failure`)
- LOG_LEVEL: (_default_ "info")
- LOG_URL: (_default_ `https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logs:`)
- HTTP_METHODS: (_default_ `['GET', 'POST', 'PUT', 'DELETE', 'HEAD']`)
- HTTP_CONTENT_TYPE: (_default_ `application/json`)
- CORS_HEADERS: (_default_ `['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'x-requested-with']`)
- CORS_ORIGINS: (_default_ `'*'`)
- CORS_X_REQUEST: (_default_ `'*'`)

