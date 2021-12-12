# deafadder-container

> An attempt to recreate the magic behind Spring, but in python.

!> This library is still in its early stage and will certainly changes over time. So, keep it's API is not stable yet
and any evolution might lead to breaking changes. **This will remain true until reaching v1.0.0**

## What it is

A simple container manager based on `metaclass`. Each container will be a singleton (but not limited to) and their
instance can easily be retrieved.

See the [Quick start](GettingStarted/quickstart.md) guide for more details.

## Why

Creating an application split into multiple service and component is somehow quite verbose in plan python.
The idea is to mimic the singleton base approach of Spring and the container management to ease the development of such
application in python.

Its quite ironic, but coming from a java/Spring background, I've always found application
development more verbose in python than in java/Spring. This library is an attempt to bring
back simplicity in python application development.

## What it is not

This is not a Spring replication. The scope is way lighter and only focus on container management.

## Features

- Create new Component
- Reuse and easily retrieve previously created Component
- Allow multiple instance of the same Component if they have a specific name attached to them
- Delete specific Component, all Component of the same type, or simply purge everything
- Auto inject Component field at Component creation (for Component that depends on other Components)
- Manage *post init* configuration