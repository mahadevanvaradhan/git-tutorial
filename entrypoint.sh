#!/bin/bash

echo "Starting the application..."

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${INPUT_EMAIL}"
git config --global safe.directory /github/workspace


python usr/bin/feed.py


git add -A && git commit -m "Update feed" || echo "No changes to commit"

git push --setupstream origin main || echo "No changes to push"

echo "Application Prodcess completed..."