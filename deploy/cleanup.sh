#!/bin/bash
set -euo pipefail

REGISTRY="http://registry:5000"
KEEP=10

apk add --no-cache curl jq

REPOS=$(curl -sS "$REGISTRY/v2/_catalog" \
  | jq -r '.repositories[]' \
  | sort)

for REPO in $REPOS; do
  echo "Processing repository: $REPO"

  TAGS=$(curl -sS "$REGISTRY/v2/$REPO/tags/list" \
    | jq -r '.tags[] // empty')

  if [ -z "$TAGS" ]; then
    echo "  No tags found, skipping."
    continue
  fi

  CREATED_TAGS=()
  while read -r TAG; do
    MANIFEST=$(curl -sS -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
      "$REGISTRY/v2/$REPO/manifests/$TAG")

    CONFIG_DIGEST=$(echo "$MANIFEST"   \
      | jq -r '.config.digest')

    CREATED=$(curl -sS "$REGISTRY/v2/$REPO/blobs/$CONFIG_DIGEST" \
      | jq -r '.created')

    CREATED=${CREATED:-1970-01-01T00:00:00Z}

    CREATED_TAGS+=("$CREATED $TAG")
  done <<< "$TAGS"

  TO_KEEP=$(printf '%s\n' "${CREATED_TAGS[@]}" \
    | sort -r \
    | head -n "$KEEP" \
    | awk '{print $2}')

  TO_DELETE=$(printf '%s\n' "${TAGS[@]}" | grep -xv -F -f <(printf '%s\n' "$TO_KEEP"))

  if [ -z "$TO_DELETE" ]; then
    echo "  All ${#TAGS[@]} tags are within the last $KEEP creations—nothing to delete."
    continue
  fi

  for TAG in $TO_DELETE; do
    echo "  Deleting $REPO:$TAG"
    DIGEST=$(curl -sSI -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
      "$REGISTRY/v2/$REPO/manifests/$TAG" \
      | awk -F': ' '/Docker-Content-Digest/ {print $2}' \
      | tr -d '\r')

    if [ -n "$DIGEST" ]; then
      curl -sS -X DELETE "$REGISTRY/v2/$REPO/manifests/$DIGEST" \
        && echo "    -> deleted digest $DIGEST"
    else
      echo "    ! could not find digest for $TAG"
    fi
  done
done

echo "Running garbage collection…"
docker exec -i "$(docker ps -qf name=registry)" \
  registry garbage-collect /etc/docker/registry/config.yml --delete-untagged=true
