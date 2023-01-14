PARENT=$HOME
(cd $PARENT/rpi_clock/bin; python3 rpi_clock.py rpi_clock.cfg 2>&1 | tee $PARENT/rpi_clock/rpi_clock.log) &

