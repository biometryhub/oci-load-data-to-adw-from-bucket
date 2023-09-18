#!/bin/bash

fn -v deploy --app test-trigger
fn invoke test-trigger load-data-to-adw-from-bucket
