#!/bin/bash
# helper script to pull deploy.sh and requirements.txt from f5-cloud-failover repository
# Environment variable(s) are required to securely execute the git remote add 
# export GIT_SERVER=gitserver.example.com
set -e

# initiate a local repository and add remote repository
git init
git remote add origin https://${GIT_SERVER}/cloudsolutions/f5-cloud-failover.git
git fetch
# checkout --merge
git checkout origin/develop -m test/functional/deployment/deploy.sh
git checkout origin/develop -m test/functional/deployment/requirements.txt

# move the files checkout to current directory
mv test/functional/deployment/requirements.txt .
mv test/functional/deployment/deploy.sh .

# perform cleanup
rm -rf test .git

