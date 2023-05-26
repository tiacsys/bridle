#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>

extern const struct gpio_dt_spec btn;
extern const struct gpio_dt_spec led;
extern const struct gpio_dt_spec led2;

#define APPLICATION_IO_INIT_PRIORITY 96
#define APPLICATION_CB_INIT_PRIORITY 97
