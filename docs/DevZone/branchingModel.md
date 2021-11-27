Branching model
===============

It will mostly follow the git flow branching model, with the little difference that there is no
need for the develop branch for this project workflow.

![logo](../assets/images/branching-model/base.svg ':size=WIDTHxHEIGHT')


Workflow
--------

Below will be the rules that each branches will follow. Those are the main rules, but exception can arise
based on circumstances (let's not be to rigid, since the workflow is there to ease the work, not to add
more complexity and waste time and effort).

The choice of this workflow is to help in automation by reducing the number of possible scenario. 
Hopefully, most of the tedious task such as deploying and increasing fix version should be easily
automated using this workflow.

### Master

The `mater` branch is the base branch which represent what is actually released and accessible.

Each new commit on `master` does not necessary mean a new release. Only merge commit from a `release` branch
will be deployed, as well as new `tag` with a valid new version will be deployed.

### release

The `release` branches are used to prepare a new release (a set of new features).
They derive directly from `master` and should be merged only to master. 

No automation expected on those branches, except the usual tests.

### feature

The `feature` branches are there to centralize the work for a specific feature.
They derive directly from the `release` that should contains this new feature and should be merged to this 
same `release` branch.

Each `feature` branches will have the reference to the jira ticket number that describe the feature.

No automation expected on those branches, except the usual tests.

### hotfix

The `hotfix` branches are there to fix an issue on `master`. 
They derive from `master` and are merged onto `master` and the current `release` branch.


Automation
----------

The automation tool used is [circle-ci](https://circleci.com/). I wanted, to have a common tool to manage different
repo (github and bitbucket), and wanted to use a docker based service so that I can use custom images.

There is 3 main workflows: *all purpose for test*, *merging from feature to master*, *merging from hotfix to master* and *tagging*

### All purpose test

As soon as there is a new commit pushed to any branches, test suites will be launched.

No other purpose than to let the developer now the status of his build.

### Merging from feature to master

* When a commit arrive on `master`
* And this commit have two parent
* And those parent are `master` and `feature/xxx`
* Then the CI will tag the commit with the appropriate version `X.Y.Z`

### Merging from hotfix to master

* When a commit arrive on `master`
* And this commit have two parent
* And those parents are `mater` and `hotfix/xxx`
* Then CI will create a new commit on master with updated bugfix version in the versions files
* And it will tag this commit with a new version tag `X.Y.Z`

### tagging

* When a new tag with the pattern `X.Y.Z` is set
* Then CI will deploy the lib to artifactory