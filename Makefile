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

make-image:
	docker build -t ${REGISTRY}/ospserver:${TAG} .

push-image:
	docker push ${REGISTRY}/ospserver:${TAG}

execute-release: make-image push-image
