#! /bin/bash

if [[ -z "${DOCKER_REG}" ]]; then
  DOCKER_REG="repository.chinanorth.cloudapp.chinacloudapi.cn"
fi

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

IMAGE_NAME="cbb/objectdetection-api"

DOCKER_IMAGE="${DOCKER_REG}/${IMAGE_NAME}:${BUILD_NUMBER}"
CNTNR_NAME="objectdetection-api"

REDIS_CNTNAME="celery_redis"

echo ${DOCKER_PASSWORD} | docker login -u "${DOCKER_USERNAME}" --password-stdin ${DOCKER_REG}

WEB_CID=$(docker ps -a -f name=${CNTNR_NAME} -q)

if [[ ! -z ${WEB_CID} ]]; then
  docker rm -f ${WEB_CID}
fi

WEB_CID=$(docker ps -a -f name=${REDIS_CNTNAME} -q)

if [[ -z ${WEB_CID} ]]; then
  docker run -itd --restart=always --name celery_redis repository.chinanorth.cloudapp.chinacloudapi.cn/cbb/redis:5.0
fi

IMAGE_ID=$(docker images ${DOCKER_IMAGE} -q)

if [[ ! -z ${IMAGE_ID} ]]; then
  docker rmi -f ${IMAGE_ID}
fi

docker run -itd --restart=always --name ${CNTNR_NAME} -v /opt/hce/idas/automl/logs:/usr/src/app/logs --link celery_redis:redis -e "objectdetection_HOST=redis" -p 15031:5031 ${DOCKER_IMAGE}
