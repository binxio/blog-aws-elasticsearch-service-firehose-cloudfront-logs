.PHONY: help init clean validate mock create delete info deploy
.DEFAULT_GOAL := help
environment = "example"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create: ## create env
	@sceptre launch-env $(environment)

delete: ## delete env
	@sceptre delete-env $(environment)

info: ## describe resources
	@sceptre describe-stack-outputs $(environment) elasticsearch

merge-lambda: ## merge lambda in api gateway
	aws-cfn-update \
		lambda-inline-code \
		--resource ProcessorFunction \
		--file lambdas/processors/identity_processor.py \
		templates/elasticsearch.yaml
	aws-cfn-update \
		lambda-inline-code \
		--resource NotificationLambda \
		--file lambdas/s3_handler/s3_cf_log_handler.py \
		templates/elasticsearch.yaml

test: ## run unit tests
	pipenv run pytest -s -v tests