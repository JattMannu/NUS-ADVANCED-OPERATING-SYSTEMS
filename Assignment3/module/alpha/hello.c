#include <linux/init.h>
#include <linux/module.h>
MODULE_LICENSE("GPL");
//Init Code
static int hello_init(void){
    //Using Linux Kernal's Print
    printk(KERN_ALERT "Hello, Manpreet!\n");
    return 0;
}

static void hello_exit(void){
    printk(KERN_ALERT "Good bye!\n");
}

//When you start this module jump to hello_init
module_init(hello_init);
//When you stop this module jump to hello_exit
module_exit(hello_exit);