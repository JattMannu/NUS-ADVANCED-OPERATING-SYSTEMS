#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/moduleparam.h> // for module_param()

MODULE_LICENSE("GPL");

static char *who = "NOT DEFINED";
/* 
 * module_param(foo, int, 0000)
 * The first param is the parameters name
 * The second param is it's data type
 * The third argument is the permissions bits, 
 */
module_param(who, charp, 0000);
MODULE_PARM_DESC(who, "Name of the user.");

static int hello_init(void)
{
printk(KERN_ALERT "Hello, %s\n", who);
return 0;
}
static void hello_exit(void)
{
printk(KERN_ALERT "Goodbye, cruel world\n");
}

module_init(hello_init);
module_exit(hello_exit);