#!/bin/bash
set -ue
# switch to root
cwd="$( cd "$( dirname "${BASH_SOURCE[0]:-${(%):-%x}}" )" >/dev/null && pwd )"; cd $cwd/..

DCO_FILE=${1:-docker-compose.yml}
platforms=("amd64" "arm64")

function dco() { docker-compose -f ${DCO_FILE} $@;}

services=( $(dco config --services) )

for i in "${!services[@]}"; do
    service="${services[$i]}"
    echo "[INFO] $(($i + 1)) of ${#services[@]} - Processing docker compose service '${service}'"
    # remove everything after @ for images with sha digests in tags
    image="$(dco config | yq -r ".services.\"${service}\".image" | cut -f1 -d"@")"
    new_image="$image"

    echo "[INFO] Image $image will contain multiple manifests/platforms"
    manifests=""
    for plt in "${platforms[@]}"; do
        echo "[INFO] Building image $image-$plt"
        echo \$ DOCKER_DEFAULT_PLATFORM=linux/$plt dco build ${service}
        # https://github.com/multiarch/qemu-user-static is required for multi-arch builds on linux
        DOCKER_DEFAULT_PLATFORM=linux/$plt dco build ${service}
        echo + docker tag ${image} ${new_image}-${plt}
        docker tag ${image} ${new_image}-${plt}
        echo + docker push ${new_image}-${plt}
        docker push ${new_image}-${plt}
        manifests="${manifests} ${new_image}-${plt} "
    done
    echo "[INFO] Creating manifest $image from $manifests"
    docker manifest rm $new_image || true
    # create manifest aggregating images for all platforms
    docker manifest create ${new_image} ${manifests}
    docker manifest inspect ${new_image}
    # verify that manifest contains all required platforms
    [[ $(docker manifest inspect ${new_image} | jq -rc '.manifests[].platform.architecture' | tr '\n' ',') == "$(printf "%s," "${platforms[@]}")" ]] || bash -c 'echo "Invalid Manifest" && exit 1'
    docker manifest push ${new_image}

done

