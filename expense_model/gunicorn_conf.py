#!/usr/bin/env python3
import os
import multiprocessing

bind = "0.0.0.0:8080"
workers = 3
#workers = multiprocessing.cpu_count() * 2 + 1
#certfile = "ssl/fullkeychain.pem"
#keyfile = "ssl/private.key"
