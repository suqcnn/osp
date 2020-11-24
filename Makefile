ENVVAR=CGO_ENABLED=0 LD_FLAGS=-s
GOOS?=linux
REGISTRY?=openspacee
TAG?=dev


build-binary: clean
	$(ENVVAR) GOOS=$(GOOS) go build -o ospserver

clean:
	rm -f ospserver

docker-builder:
	docker images | grep ospserver-builder || docker build -t ospserver-builder ./builder

build-in-docker: clean docker-builder
	docker run -v `pwd`:/gopath/src/github.com/openspacee/osp/ ospserver-builder:latest bash -c 'cd /gopath/src/github.com/openspacee/osp && make build-binary'

make-base-image:
	docker build -t openspacee/ospserver-base ./base-image

make-image: build-in-docker make-base-image
	docker build -t ${REGISTRY}/osp:${TAG} .

push-image:
	docker push ${REGISTRY}/osp:${TAG}

execute-release: make-image push-image
