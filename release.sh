#!/bin/bash
# Release script for Konflux Chatbot MCP
# Usage: ./release.sh [version]
# Example: ./release.sh 1.0.1

set -e

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get version from argument or VERSION file
if [ -n "$1" ]; then
    VERSION="$1"
else
    VERSION=$(cat VERSION)
fi

IMAGE_NAME="quay.io/dhshah/konflux"

echo -e "${YELLOW}Building version ${VERSION}...${NC}"

# Build the image
podman build -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:v${VERSION} .

echo -e "${YELLOW}Pushing to quay.io...${NC}"

# Push both tags
podman push ${IMAGE_NAME}:latest
podman push ${IMAGE_NAME}:v${VERSION}

# Update VERSION file if new version was passed
if [ -n "$1" ]; then
    echo "${VERSION}" > VERSION
    echo -e "${GREEN}Updated VERSION file to ${VERSION}${NC}"
fi

echo -e "${GREEN}✅ Successfully released version ${VERSION}${NC}"
echo -e "${GREEN}✅ Users can now pull: podman pull ${IMAGE_NAME}:latest${NC}"
echo ""
echo "Tagged versions:"
echo "  - ${IMAGE_NAME}:latest"
echo "  - ${IMAGE_NAME}:v${VERSION}"

