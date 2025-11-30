#!/bin/bash

mkdir -p ~/funsearch/data
mkdir -p ~/funsearch/data/scores ~/funsearch/data/graphs ~/funsearch/data/backups
mkdir -p ~/funsearch/examples

# 현재 사용자 정보
IMAGE_NAME="funsearch:$(whoami)"

# 이미지가 없으면 빌드
if [[ "$(docker images -q ${IMAGE_NAME} 2> /dev/null)" == "" ]]; then
    echo "Building Docker image for user $(whoami)..."
    docker build \
        --build-arg USER_ID=$(id -u) \
        --build-arg GROUP_ID=$(id -g) \
        --build-arg USERNAME=$(whoami) \
        -t ${IMAGE_NAME} .

    if [ $? -ne 0 ]; then
        echo "Error: Docker build failed"
        exit 1
    fi
fi

# 환경 변수 로드
if [ -f .env ]; then
    source .env
else
    echo "Warning: .env file not found"
fi

# 컨테이너 실행
echo "Starting funsearch container for user $(whoami)..."
echo "Working directory: /home/$(whoami)/workspace"
echo "Host data directory: $(pwd)"

docker run -it \
    -v $(pwd):/home/$(whoami)/workspace \
    --env-file .env \
    ${IMAGE_NAME}

