#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting ideacli release process...${NC}"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: pyproject.toml not found${NC}"
    exit 1
fi

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info/

# Update version to 0.1.3 (macOS compatible sed)
echo -e "${YELLOW}Updating version to 0.1.3...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' 's/version = "[^"]*"/version = "0.1.3"/' pyproject.toml
else
    # Linux
    sed -i 's/version = "[^"]*"/version = "0.1.3"/' pyproject.toml
fi

# Verify version was updated
if grep -q 'version = "0.1.3"' pyproject.toml; then
    echo -e "${GREEN}✓ Version updated successfully${NC}"
else
    echo -e "${RED}✗ Failed to update version${NC}"
    exit 1
fi

# Build the package
echo -e "${YELLOW}Building package...${NC}"
python -m build

# Check if build was successful
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo -e "${RED}✗ Build failed - no dist directory or empty${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Build completed successfully${NC}"
echo -e "${YELLOW}Files in dist/:${NC}"
ls -la dist/

# Upload to PyPI
echo -e "${YELLOW}Uploading to PyPI...${NC}"
twine upload dist/*

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Release 0.1.3 completed successfully!${NC}"
    echo -e "${GREEN}Package available at: https://pypi.org/project/ideacli/0.1.3/${NC}"
else
    echo -e "${RED}✗ Upload failed${NC}"
    exit 1
fi

# Tag the release
echo -e "${YELLOW}Creating git tag...${NC}"
git add pyproject.toml
git commit -m "Release v0.1.3" || echo "No changes to commit"
git tag -a v0.1.3 -m "Release version 0.1.3"

echo -e "${GREEN}✓ Git tag created${NC}"
echo -e "${YELLOW}Don't forget to push the tag: git push origin v0.1.3${NC}"
