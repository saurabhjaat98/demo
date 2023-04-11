###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################

# Usage:
#   Use the git targets to perform git operation
#   make git-new-branch b=<branch-name>: Creates new branch
#   make git-rebase: Rebase the current branch with main
#   make git-pre-commit: Run the pre-commit checks
#   make git-commit m='<commit-msg>: Commits the current branch
#   make git-commit-amend: Commits the current branch with amend
#   make git-push: Push the current branch to remote
#   make git-delete-all: Delete all your local branch except main and current
#   make run: Run the CCP application
#   make docker-check: Check the application is working properly using docker container
#   make setup: For setup the CCP Middleware application
#   make docker run: For start CCP Middleware application


BRANCH_NAME_REGEX = ^CIRRUS-\d\+$
COMMIT_MESSAGE_REGEX = ^CIRRUS-\d\+\:

b ?= $(shell git branch | grep \* | cut -d ' ' -f2) # branch name if provided otherwise pick the current branch
m ?= "" # commit message
current_time := $(shell date +'%F %T')

git-new-branch:
	@if echo "$(b)" | grep -q "$(BRANCH_NAME_REGEX)"; then \
		git checkout -b $(b); \
	else \
		echo "Branch name is not matching with pattern '$(BRANCH_NAME_REGEX)'"; \
	fi


# Does rebase current branch with remote's main branch
git-rebase:
	git stash
	git checkout main
	git pull origin main
	git checkout $(b)
	git rebase main
	git stash apply
	git stash drop

# Run the pre commit checks
git-pre-commit: test
	echo "Running pre-commit checks for $(b) branch at $(current_time)"
	pre-commit run --all-files


# Does git commit but check if commit message is matching with pattern COMMIT_MESSAGE_REGEX
git-commit: git-pre-commit
	@if echo "$(m)" | grep -q "$(COMMIT_MESSAGE_REGEX)"; then \
  		echo "Running pre-commit checks for $(b) branch at $(current_time)"; \
		git add .; \
		git commit -m"$(m)"; \
	else \
	  	echo "$(m)"; \
		echo "Commit message should follow this pattern $(COMMIT_MESSAGE_REGEX)"; \
	fi


# Does commit amend
git-commit-amend: git-pre-commit
	echo "Running pre-commit checks for $(b) branch at $(current_time)"
	git add .
	git commit --amend --no-edit



# Does git push to remote
git-push:
	git push origin $(b)

# Does git push to remote
git-push-force:
	git push origin $(b) -f


# Delete all your local branches except main and current
git-delete-all:
	git branch | grep -v "main\|$(b)" | xargs git branch -D


# For mac only
# Setup for CCP application
setup:
	brew install python@3.10
	brew install docker
	docker-compose up -d mongo redis
	virtualenv .venv --python python3.10

# Run the CCP application
run:
	docker-compose up -d mongo redis
	pip install -r requirements.txt
	uvicorn ccp_server.main:app --reload

# Run Tests
test:
	python3 setup.py install
	python3 tests/runner.py

# Run the application inside docker container
docker-run:
	docker-compose up -d --build

# Check the application is working properly using docker container
docker-check:
	docker build -t ccp-app .
	docker run -d -p 7080:7080 --name ccp-container ccp-app
	sleep 10
	curl 'http://localhost:7080/health'
	docker stop ccp-container
	docker rm ccp-container
	docker rmi ccp-app -f
