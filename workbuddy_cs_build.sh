#!/bin/bash -

# Prepare the WorkBuddy container.

# strict error handling
set -o pipefail  # trace ERR through pipes
set -o errtrace  # trace ERR through 'time command' and other functions
set -o nounset   # set -u : exit the script if you try to use an uninitialized variable
set -o errexit   # set -e : exit the script if any statement returns a non-true return value

echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Welcome to the WorkBuddy image preparation script."

echo "$(date +'%0Y-%0m-%0d %0R:%0S'): We delete any potentially existing old images."
docker image rm workbuddy_cs || true
docker image rm workbuddy_cs || true

echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now we build the computer science image."
docker build --progress=plain -t workbuddy_cs .

echo "$(date +'%0Y-%0m-%0d %0R:%0S'): All done."
