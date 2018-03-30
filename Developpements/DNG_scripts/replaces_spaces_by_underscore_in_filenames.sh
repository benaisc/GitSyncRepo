#!/bin/bash

# Naive recursive version assuming there is no spaces in subdirectory names

shopt -s globstar

for f in **/*\ *; do mv "$f" "${f// /_}"; done
