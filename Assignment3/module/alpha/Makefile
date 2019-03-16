obj-m := hello.o	# Module Name is hello.c

KDIR  := /lib/modules/$(shell uname -r)/build

all:
	$(MAKE) -C $(KDIR) M=$(shell pwd) modules

clean:
	$(MAKE) -C $(KDIR) M=$(shell pwd) clean
	$(RM) Module.markers modules.order