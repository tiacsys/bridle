/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mfd_sipomuxgp.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sipomuxgp, CONFIG_MFD_LOG_LEVEL);

/*
 * multi functional interface --- main entries
 */

int mfd_sipomuxgp_num_bits(const struct device *dev)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;

	return config->num_bits;
}

static int mfd_sipomuxgp_get_bit(const struct device *dev,
				 uint32_t bit, uint8_t *value);

int mfd_sipomuxgp_bits(const struct device *dev, size_t offs, uint32_t *val)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;

	if (offs >= (config->num_bits - NUM_BITS(uint32_t))) {
		LOG_ERR("%s: invalid number of offset: got=%u, expected<%u",
			dev->name, offs, config->num_bits - NUM_BITS(uint32_t));
		return -EINVAL;
	}

	for (size_t idx = 0; idx < 32; idx++) {
		uint8_t bit_val = 0;

		mfd_sipomuxgp_get_bit(dev, idx + offs, &bit_val);
		*val |= (bit_val << idx);
	}

	return 0;
}

static int mfd_sipomuxgp_set_bit(const struct device *dev,
				 uint32_t bit, uint8_t value);

int mfd_sipomuxgp_bit_on(const struct device *dev, size_t bit)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;

	if (bit >= config->num_bits) {
		LOG_ERR("%s: invalid number of bit: got=%u, expected<%u",
			dev->name, bit, config->num_bits);
		return -EINVAL;
	}

	return mfd_sipomuxgp_set_bit(dev, bit, 100);
}

int mfd_sipomuxgp_bit_off(const struct device *dev, size_t bit)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;

	if (bit >= config->num_bits) {
		LOG_ERR("%s: invalid number of bit: got=%u, expected<%u",
			dev->name, bit, config->num_bits);
		return -EINVAL;
	}

	return mfd_sipomuxgp_set_bit(dev, bit, 0);
}

int mfd_sipomuxgp_xy_on(const struct device *dev, size_t x, size_t y)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	size_t bit = x + y * config->columns;

	if (x >= config->columns) {
		LOG_ERR("%s: invalid number of x: got=%u, expected<%u",
			dev->name, x, config->columns);
		return -EINVAL;
	}

	if (y >= config->rows) {
		LOG_ERR("%s: invalid number of y: got=%u, expected<%u",
			dev->name, y, config->rows);
		return -EINVAL;
	}

	return mfd_sipomuxgp_bit_on(dev, bit);
}

int mfd_sipomuxgp_xy_off(const struct device *dev, size_t x, size_t y)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	size_t bit = x + y * config->columns;

	if (x >= config->columns) {
		LOG_ERR("%s: invalid number of x: got=%u, expected<%u",
			dev->name, x, config->columns);
		return -EINVAL;
	}

	if (y >= config->rows) {
		LOG_ERR("%s: invalid number of y: got=%u, expected<%u",
			dev->name, y, config->rows);
		return -EINVAL;
	}

	return mfd_sipomuxgp_bit_off(dev, bit);
}

int mfd_sipomuxgp_output_ratio(const struct device *dev, uint8_t percent)
{
	mfd_sipomuxgp_data_t * const data = dev->data;
	k_spinlock_key_t key;

	if (percent > 100) {
		return -EINVAL;
	}

	key = k_spin_lock(&data->lock);
	data->oe_noblank = (percent > 0);
	data->oe_noratio = (percent > 50);
	k_spin_unlock(&data->lock, key);

	return 0;
}

/*
 * default data changing --- manipulate the bit matrix buffer
 */

static int mfd_sipomuxgp_get_bit(const struct device *dev,
				 uint32_t bit, uint8_t *value)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	mfd_sipomuxgp_data_t * const data = dev->data;
	k_spinlock_key_t key;

	if (!value) {
		return -EINVAL;
	}

	key = k_spin_lock(&data->lock);

	uint8_t byte = data->bitbuf[__BITBUF_IDX(bit, config->columns)];
	uint8_t bitv = (byte >> __BITBUF_BIT(bit, config->columns));
	*value = bitv & 1;

	k_spin_unlock(&data->lock, key);
	return 0;
}

static int mfd_sipomuxgp_set_bit(const struct device *dev,
				 uint32_t bit, uint8_t value)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	mfd_sipomuxgp_data_t * const data = dev->data;
	k_spinlock_key_t key;

	if (value > 100) {
		return -EINVAL;
	}

	key = k_spin_lock(&data->lock);

	if (value > 0) {
		data->bitbuf[__BITBUF_IDX(bit, config->columns)]
			|= BIT(__BITBUF_BIT(bit, config->columns));
	} else {
		data->bitbuf[__BITBUF_IDX(bit, config->columns)]
			&= ~BIT(__BITBUF_BIT(bit, config->columns));
	}

	LOG_HEXDUMP_DBG(data->bitbuf, data->bitbuf_sz, "bitbuf");

	k_spin_unlock(&data->lock, key);
	return 0;
}

/*
 * default data output prcessing --- calling the data transfer from backend
 */

static void mfd_sipomuxgp_process(const struct device *dev)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	mfd_sipomuxgp_data_t * const data = dev->data;
	uint8_t *col_data;
	size_t col_count;
	k_spinlock_key_t key;

	key = k_spin_lock(&data->lock);

	col_count = __TOTAL_BYTES(config->columns);
	col_data = &data->bitbuf[data->row_count * col_count];

	config->backend.xfr_data(dev, data->row_count, col_data, col_count,
				      data->padding_sz);

	if (++data->row_count >= config->rows) {
		data->row_count = 0;
		data->oe_count++;
	}

	k_spin_unlock(&data->lock, key);
}

/*
 * default signal handling --- configure and setup hardware signals
 */

static int mfd_sipomuxgp_set_oe(const struct device *dev, const uint8_t value)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	mfd_sipomuxgp_data_t * const data = dev->data;
	uint8_t enable;
	int ret;

	enable = value && data->oe_noblank &&
		 (data->oe_noratio || (data->oe_count % 2));
	ret = gpio_pin_set_dt(&config->enable, enable);
	if (ret < 0) {
		LOG_ERR("%s: can't %s output!", dev->name,
			value ? "enable" : "disable");
		return ret;
	}

	return 0;
}

static int mfd_sipomuxgp_set_addr(const struct device *dev, const uint8_t addr)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	int ret;

	for (size_t addr_bit = 0; addr_bit < config->num_addr; addr_bit++) {

		ret = gpio_pin_set_dt(&config->addr[addr_bit],
				      ((addr >> addr_bit) & 1));
		if (ret < 0) {
			LOG_ERR("%s: can't change address bit %u!", dev->name,
				addr_bit);
			return ret;
		}
	}

	return 0;
}

static int mfd_sipomuxgp_cfg_oe(const struct device *dev)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	int ret;

	if (!gpio_is_ready_dt(&config->enable)) {
		LOG_ERR("%s: GPIO pin: %s not ready", dev->name,
			config->enable.port ? config->enable.port->name :
					      "null");
		return -ENODEV;
	}

	ret = gpio_pin_configure_dt(&config->enable, GPIO_OUTPUT_INACTIVE);
	if (ret < 0) {
		LOG_ERR("%s: can't configure enable pin %d as output",
			dev->name, config->enable.pin);
		return ret;
	}

	LOG_DBG("%s: ready with GPIO enable over %s at pin %d!", dev->name,
		config->enable.port ? config->enable.port->name : "null",
		config->enable.pin);
	return 0;
}

static int mfd_sipomuxgp_cfg_addr(const struct device *dev)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	int ret;

	for (size_t addr_idx = 0; addr_idx < config->num_addr; addr_idx++) {
		if (!gpio_is_ready_dt(&config->addr[addr_idx])) {
			LOG_ERR("%s: GPIO pin: %s not ready", dev->name,
				config->addr[addr_idx].port ?
				config->addr[addr_idx].port->name : "null");
			return -ENODEV;
		}

		ret = gpio_pin_configure_dt(&config->addr[addr_idx],
					    GPIO_OUTPUT_INACTIVE);
		if (ret < 0) {
			LOG_ERR("%s: can't configure address pin %d as output",
				dev->name, config->addr[addr_idx].pin);
			return ret;
		}

		LOG_DBG("%s: ready with GPIO address bit %d over %s at pin %d!",
			dev->name, addr_idx, config->addr[addr_idx].port ?
			config->addr[addr_idx].port->name : "null",
			config->addr[addr_idx].pin);
	}
	return 0;
}

/*
 * internal driver mechanic --- timed worker to tirgger the refresh processing
 */

static void mfd_sipomuxgp_refresh_worker(struct k_work *work)
{
	mfd_sipomuxgp_data_t * const data =
	CONTAINER_OF(work, mfd_sipomuxgp_data_t, refresh_worker);

	/* Processing the SIPO/MOX data, put out the data on hardware. */
	mfd_sipomuxgp_process(data->dev);
}

static void mfd_sipomuxgp_refresh_timer(struct k_timer *timer)
{
	mfd_sipomuxgp_data_t * const data =
	CONTAINER_OF(timer, mfd_sipomuxgp_data_t, refresh_timer);

	/* Submit the SIPO/MOX data processing worker to the system queue. */
	k_work_submit_to_queue(&mfd_sipomuxgp_xfr_workq, &data->refresh_worker);
}

/*
 * driver initialization --- configure and setup internal driver mechanic
 */

static int mfd_sipomuxgp_init(const struct device *dev)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	mfd_sipomuxgp_data_t * const data = dev->data;
	k_spinlock_key_t key;
	int ret;

	ret = config->backend.init(dev);
	if (ret < 0) {
		return ret;
	}

	key = k_spin_lock(&data->lock);

	if (config->num_bits != config->columns * config->rows) {
		LOG_ERR("%s: invalid columns (%u) or rows (%u)",
			dev->name, config->columns, config->rows);
		return -EINVAL;
	}

	data->row_count = 0;
	data->dev = dev;

	k_work_init(&data->refresh_worker, mfd_sipomuxgp_refresh_worker);
	k_timer_init(&data->refresh_timer, mfd_sipomuxgp_refresh_timer, NULL);
	k_timer_start(&data->refresh_timer, K_NO_WAIT,
					    K_USEC(data->refresh_time_us));

	k_spin_unlock(&data->lock, key);

	LOG_DBG("%s: ready for %u x %u (%u) bit!", dev->name,
		config->rows, config->columns, config->num_bits);
	LOG_DBG("%s: - with bit buffer of %u byte%s", dev->name,
		data->bitbuf_sz, data->bitbuf_sz > 1 ? "s" : "");
	LOG_DBG("%s: - with zero padding of %u byte%s", dev->name,
		data->padding_sz, data->padding_sz > 1 ? "s" : "");
	return 0;
}

#ifdef CONFIG_PM_DEVICE
static int mfd_sipomuxgp_pm_device_pm_action(const struct device *dev,
					     enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#define INST_DT_SIPOMUXGP(n, b) DT_INST(n, sipo_mux_gp_##b)

#define MFD_SIPOMUXGP_CTX_SPEC_ELEM(_node_id, _prop, _idx)                  \
	GPIO_DT_SPEC_GET_BY_IDX(_node_id, _prop, _idx),

#define MFD_SIPOMUXGP_CTX_FOREACH_ELEM(n, b, p)                             \
	DT_FOREACH_PROP_ELEM(INST_DT_SIPOMUXGP(n, b), p,                    \
			     MFD_SIPOMUXGP_CTX_SPEC_ELEM)

#define MFD_SIPOMUXGP_CTX_GPIOS_ADDR(n, b)                                  \
	(const struct gpio_dt_spec[]){                                      \
		MFD_SIPOMUXGP_CTX_FOREACH_ELEM(n, b, addr_gpios)            \
	}

#define MFD_SIPOMUXGP_CTX_GPIO_ENABLE(n, b)                                 \
	GPIO_DT_SPEC_GET_OR(INST_DT_SIPOMUXGP(n, b), oe_gpios, {0})

#define MFD_SIPOMUXGP_CTX_NUM_ADDR(n, b)                                    \
	DT_PROP_LEN(INST_DT_SIPOMUXGP(n, b), addr_gpios)

#define MFD_SIPOMUXGP_CTX_ROWS(n, b)                                        \
	BIT(MFD_SIPOMUXGP_CTX_NUM_ADDR(n, b))

#define MFD_SIPOMUXGP_CTX_COLUMNS(n, b)                                     \
	DT_PROP(INST_DT_SIPOMUXGP(n, b), data_width)

#define MFD_SIPOMUXGP_CTX_NUM_BITS(n, b)                                    \
	(MFD_SIPOMUXGP_CTX_ROWS(n, b) * MFD_SIPOMUXGP_CTX_COLUMNS(n, b))

#define MFD_SIPOMUXGP_CTX_BITBUF_SZ(n, b)                                   \
	(__TOTAL_BYTES(MFD_SIPOMUXGP_CTX_NUM_BITS(n, b)))

#define MFD_SIPOMUXGP_CTX_BITBUF(n, b)                                      \
	(uint8_t [(MFD_SIPOMUXGP_CTX_BITBUF_SZ(n, b))]) {}

#define MFD_SIPOMUXGP_CTX_SHIFTING(n, b)                                    \
	DT_PROP(INST_DT_SIPOMUXGP(n, b), shift_width)

#define MFD_SIPOMUXGP_CTX_PADDING(n, b)                                     \
	(MFD_SIPOMUXGP_CTX_SHIFTING(n, b) - MFD_SIPOMUXGP_CTX_COLUMNS(n, b))

#define MFD_SIPOMUXGP_CTX_PADDING_SZ(n, b)                                  \
	(__TOTAL_BYTES(MFD_SIPOMUXGP_CTX_PADDING(n, b)))

#define MFD_SIPOMUXGP_CTX_RFSTIME(n, b)                                     \
	DT_PROP(INST_DT_SIPOMUXGP(n, b), refresh_time_us)

#define MFD_SIPOMUXGP_CTX_BACKEND(n, b) {                                   \
		.config = (const void *)&mfd_sipomuxgp_##b##_config_##n,    \
		.init = mfd_sipomuxgp_##b##_init,                           \
		.cfg_oe = mfd_sipomuxgp_##b##_cfg_oe,                       \
		.cfg_addr = mfd_sipomuxgp_##b##_cfg_addr,                   \
		.set_oe = mfd_sipomuxgp_##b##_set_oe,                       \
		.set_addr = mfd_sipomuxgp_##b##_set_addr,                   \
		.xfr_data = mfd_sipomuxgp_##b##_transmit,                   \
	}


#define SIPOMUXGP_INIT(n, b)                                                \
	MFD_SIPOMUXGP_##b##_CFG_INIT(n, b);                                 \
                                                                            \
	static const mfd_sipomuxgp_config_t mfd_sipomuxgp_config_##n = {    \
		.addr = MFD_SIPOMUXGP_CTX_GPIOS_ADDR(n, b),                 \
		.enable = MFD_SIPOMUXGP_CTX_GPIO_ENABLE(n, b),              \
		.num_addr = MFD_SIPOMUXGP_CTX_NUM_ADDR(n, b),               \
		.num_bits = MFD_SIPOMUXGP_CTX_NUM_BITS(n, b),               \
		.columns = MFD_SIPOMUXGP_CTX_COLUMNS(n, b),                 \
		.rows = MFD_SIPOMUXGP_CTX_ROWS(n, b),                       \
		.backend = MFD_SIPOMUXGP_CTX_BACKEND(n, b),                 \
	};                                                                  \
                                                                            \
	BUILD_ASSERT(500 <= MFD_SIPOMUXGP_CTX_RFSTIME(n, b),                \
		"Bad refresh time, refresh-time-us must be >= 500 usec");   \
                                                                            \
	BUILD_ASSERT(0 < MFD_SIPOMUXGP_CTX_ROWS(n, b),                      \
		"Bad rows, addr-gpios needs at least one entry");           \
                                                                            \
	BUILD_ASSERT(8 <= MFD_SIPOMUXGP_CTX_COLUMNS(n, b),                  \
		"Bad columns, data-width must be equal or greater than 8"); \
                                                                            \
	BUILD_ASSERT(MFD_SIPOMUXGP_CTX_COLUMNS(n, b)                        \
		     <= MFD_SIPOMUXGP_CTX_SHIFTING(n, b),                   \
		"Too many bits, data-width does not fit into shift-width"); \
                                                                            \
	static mfd_sipomuxgp_data_t mfd_sipomuxgp_data_##n = {              \
		.refresh_time_us = MFD_SIPOMUXGP_CTX_RFSTIME(n, b),         \
		.padding_sz = MFD_SIPOMUXGP_CTX_PADDING_SZ(n, b),           \
		.bitbuf_sz = MFD_SIPOMUXGP_CTX_BITBUF_SZ(n, b),             \
		.bitbuf = MFD_SIPOMUXGP_CTX_BITBUF(n, b),                   \
		.oe_noblank = true,                                         \
		.oe_noratio = true,                                         \
		.oe_count = 0,                                              \
	};                                                                  \
                                                                            \
	PM_DEVICE_DT_DEFINE(INST_DT_SIPOMUXGP(n, b),                        \
			    mfd_sipomuxgp_pm_device_pm_action);             \
                                                                            \
	DEVICE_DT_DEFINE(INST_DT_SIPOMUXGP(n, b), mfd_sipomuxgp_init,       \
			 PM_DEVICE_DT_GET(INST_DT_SIPOMUXGP(n, b)),         \
			 &mfd_sipomuxgp_data_##n,                           \
			 &mfd_sipomuxgp_config_##n, POST_KERNEL,            \
			 CONFIG_MFD_SIPOMUXGP_INIT_PRIORITY, NULL)

#define DT_INST_FOREACH_SIPOMUXGP_STATUS_OKAY(b) LISTIFY(                   \
	DT_NUM_INST_STATUS_OKAY(sipo_mux_gp_##b), SIPOMUXGP_INIT, (;), b)

#ifdef CONFIG_MFD_SIPOMUXGP_SPI
#include "mfd_sipomuxgp_spi.h"
#define mfd_sipomuxgp_spi_cfg_oe mfd_sipomuxgp_cfg_oe
#define mfd_sipomuxgp_spi_cfg_addr mfd_sipomuxgp_cfg_addr
#define mfd_sipomuxgp_spi_set_oe mfd_sipomuxgp_set_oe
#define mfd_sipomuxgp_spi_set_addr mfd_sipomuxgp_set_addr
DT_INST_FOREACH_SIPOMUXGP_STATUS_OKAY(spi);
#endif
