#!/bin/bash
project_path=/home/ec2-user/BlockChain

pushd ${project_path}
    docker-compose down
    image_id=`docker images | grep "blockchain_web" | awk '{print $3}'`
    docker rmi ${image_id}
    git reset --hard HEAD^ && git clean -xdf && git pull
    docker-compose build && docker-compose up -d
popd


