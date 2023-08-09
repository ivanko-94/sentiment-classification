.ONESHELL:

CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

init: ## Create a conda environment
	conda create -n text-classification python=3.8
	$(CONDA_ACTIVATE) text-classification

generated: ## Build gRPC files from proto definitions
	rm -rf generated
	pip install grpcio-tools
	mkdir -p generated
	python -m grpc_tools.protoc --python_out . --grpc_python_out . --proto_path generated=./proto ./proto/*.proto --experimental_allow_proto3_optional

service: ## Build a backend classification service
	docker build -t sentiment_classification_service:1.0 -f dockerfiles/Dockerfile.service .

webapp: ## Build a docker image for the webapp client
	docker build -t sentiment_classification_webapp:1.0 -f dockerfiles/Dockerfile.webapp .

up: ## Start the service
	docker-compose up