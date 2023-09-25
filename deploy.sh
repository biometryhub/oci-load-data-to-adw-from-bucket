#!/bin/bash

fn -v deploy --no-cache --app test-trigger

git add ./func.yaml
git commit -m 'update version'
git push
