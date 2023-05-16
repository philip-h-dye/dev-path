#!/bin/bash

invoke clean \
    && invoke build \
    && python -m pip install . \
    && invoke clean

