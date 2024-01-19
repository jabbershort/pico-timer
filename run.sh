#!/bin/bash
set -e
cd build/ && cmake ..
cd src/ && make
sudo openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000" -c "program timer.elf verify reset exit"
