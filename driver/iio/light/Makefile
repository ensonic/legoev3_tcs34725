# sources taken from
# https://github.com/ev3dev/ev3-kernel/blob/ev3dev-jessie/drivers/iio/light/tcs3472.c
# https://raw.githubusercontent.com/ev3dev/ev3-kernel/ev3dev-jessie/drivers/iio/light/tcs3472.c

obj-m := tcs3472.o
KVERSION := $(shell uname -r)

# FIXME: we should not need this, could be due to
# https://github.com/ev3dev/ev3dev/issues/806
CFLAGS_tcs3472.o := -DCONFIG_SPARSE_IRQ

all:
	$(MAKE) -C /lib/modules/$(KVERSION)/build M=$(PWD) modules

clean:
	$(MAKE) -C /lib/modules/$(KVERSION)/build M=$(PWD) clean

