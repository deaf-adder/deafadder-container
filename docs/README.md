# deafadder-container

> An attempt to recreate the magic behind Spring, but in python.

!> This library is still in its early stage and will certainly changes over time. So, keep it's API is not stable yet
and any evolution might lead to breaking changes. **This will remain true until reaching v1.0.0**

## What it is

A simple container manager based on `metaclass`. Each container will be a singleton (but not limited to) and their
instance can easily be retrieved.

See the [Quick start](quickstart.md) guide for more details.

## Why

Creating an application splat into multiple service and component is somehow quite verbose in plan python.
The idea is to mimic the singleton base approach of Spring and the container management to ease the development of such
application in python.

## What it is not

This is not a Spring replication. The scope is way lighter and only focus on container management.

For now, it does not support the dependency injection like Spring and this has to be done manually for now.

## Features

- Create new container
- Reuse and easily retrieve previously created container
- Allow multiple instance of the same container if they have a specific name attached to them
- Delete specific container