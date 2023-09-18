#!/bin/bash

fn -v deploy --no-cache --app test-trigger
fn invoke test-trigger load-data-to-adw-from-bucket
