#!/usr/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ -z "${DOCKER_REG}" ]]; then
    DOCKER_REG="idas.chinaeast.cloudapp.chinacloudapi.cn"
fi

DOCKER_IMAGE_NAME="cbb/objectdetection-api"
DOCKER_IMAGE_TAG=":${BUILD_NUMBER}"

DOCKER_IMAGE="${DOCKER_REG}/${DOCKER_IMAGE_NAME}${DOCKER_IMAGE_TAG}"
BASE_IMAGE="${DOCKER_REG}/${DOCKER_IMAGE_NAME}:base"

ARTIFACT="automl-api-build-${BUILD_NUMBER}.tar.gz"
ARTIFACT_SHA="automl-api-build-${BUILD_NUMBER}.tar.gz.sha256"

function upload_artifacts() {
  docker run --rm -v $PWD:/tmp ${DOCKER_IMAGE} bash -c "cd /root && tar zcf packages.tar.gz .local && mv packages.tar.gz /tmp"
  docker run --rm -v $PWD:/tmp ${DOCKER_IMAGE} bash -c "cd /usr/src && tar zcf binary.tar.gz * && mv binary.tar.gz /tmp"

  tar zcf ${ARTIFACT} packages.tar.gz binary.tar.gz
  sha256sum ${ARTIFACT} > ${ARTIFACT_SHA}
  CHECKSUM=$(cut -c 1-64 < ${ARTIFACT_SHA})
  curl -uipredict:${IPREDICT_KEY} -X PUT "http://10.0.0.7:10081/artifactory/ipredict/automl-api/${BUILD_NUMBER}/${ARTIFACT}" -T ${ARTIFACT}
  curl -uipredict:${IPREDICT_KEY} -H "X-Checksum-Deploy:true" -H "X-Checksum-Sha256:${CHECKSUM}" -X PUT "http://10.0.0.7:10081/artifactory/ipredict/automl-api/${BUILD_NUMBER}/${ARTIFACT}"
  rm -f packages.tar.gz binary.tar.gz
}

function clean() {
  IMAGE_ID=$(docker image ls -q "${DOCKER_REG}/${DOCKER_IMAGE_NAME}:latest")
  if [[ ! -z ${IMAGE_ID} ]]; then
    docker rmi -f "${DOCKER_REG}/${DOCKER_IMAGE_NAME}:latest"
  fi
  docker rmi -f ${DOCKER_IMAGE}
  docker image prune -f
  docker container prune -f
}

function deploy() {
  ssh -i ~/.ssh/id_rsa H230809@10.0.0.4 "export DOCKER_USERNAME=${DOCKER_USERNAME} && export DOCKER_PASSWORD=${DOCKER_PASSWORD} && export BUILD_NUMBER=${BUILD_NUMBER} && bash -s" < deploy.sh
  ret=$?
  if [[ 0 != ${ret} ]]; then
    echo "Failed to deploy the API container."
    exit ${ret}
  fi
}

function build_image() {
  docker build . --no-cache -t ${DOCKER_IMAGE}
  ret=$?
  if [[ 0 != ${ret} ]]; then
    echo "Failed to build image ${DOCKER_IMAGE}."
    exit ${ret}
  fi

  # docker login before push image
  echo ${DOCKER_PASSWORD} | docker login -u "${DOCKER_USERNAME}" --password-stdin ${DOCKER_REG}

  docker push ${DOCKER_IMAGE}
  ret=$?
  if [[ 0 != ${ret} ]]; then
    echo "Failed to push image ${DOCKER_IMAGE} to the Registry"
    exit ${ret}
  fi
}

function build_base_image() {
  IMAGE_ID=$(docker image ls -q ${BASE_IMAGE})
  if [[ -z ${IMAGE_ID} ]]; then
    docker build --no-cache -f Dockerfile.base -t ${BASE_IMAGE} .
  else
    CHANGE_LIST=$(git diff --name-only ${GIT_PREVIOUS_COMMIT} ${GIT_COMMIT})
    if [[ ${CHANGE_LIST} =~ 'requirements.txt' ]]; then
      docker rmi -f ${IMAGE_ID}
      docker build --no-cache -f Dockerfile.base -t ${BASE_IMAGE} .
    fi
  fi
}

cd ${BASEDIR}

sed -i '/unittest-xml-reporting/d' requirements.txt

build_base_image

build_image

clean

# deploy

# Temporarily disable artifacts uploading
# upload_artifacts
