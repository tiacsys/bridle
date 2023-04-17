/**
 * @file drivers/actuator.h
 *
 * @brief Public APIs for the actuator driver.
 */

/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef BRIDLE_INCLUDE_DRIVERS_ACTUATOR_H_
#define BRIDLE_INCLUDE_DRIVERS_ACTUATOR_H_

/**
 * @brief Actuator Interface
 * @defgroup actuator_interface Actuator Interface
 * @ingroup io_interfaces
 * @{
 */

#include <zephyr/types.h>
#include <zephyr/device.h>
#include <errno.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Actuator channels.
 */
enum actuator_channel {
	/** De-/Acceleration on the 1st engine (0), in m/s^2 or degr/s^2. */
	ACTUATOR_CHAN_ACCEL_E0,
	/** De-/Acceleration on the 2nd engine (1), in m/s^2 or degr/s^2. */
	ACTUATOR_CHAN_ACCEL_E1,
	/** De-/Acceleration on the 3rd engine (2), in m/s^2 or degr/s^2. */
	ACTUATOR_CHAN_ACCEL_E2,
	/** De-/Acceleration on the 4th engine (3), in m/s^2 or degr/s^2. */
	ACTUATOR_CHAN_ACCEL_E3,
	/** De-/Acceleration on all the engines. */
	ACTUATOR_CHAN_ACCEL_EALL,

	/** All channels. */
	ACTUATOR_CHAN_ALL,

	/**
	 * Number of all common actuator channels.
	 */
	ACTUATOR_CHAN_COMMON_COUNT,

	/**
	 * This and higher values are actuator specific.
	 * Refer to the actuator header file.
	 */
	ACTUATOR_CHAN_PRIV_START = ACTUATOR_CHAN_COMMON_COUNT,

	/**
	 * Maximum value describing an actuator channel type.
	 */
	ACTUATOR_CHAN_MAX = INT16_MAX,
};

/**
 * @brief Actuator attribute types.
 */
enum actuator_attribute {
	/**
	 * The actuator value returned will be altered by the amount indicated
	 * by offset: final_value = actuator_value + offset.
	 */
	ACTUATOR_ATTR_OFFSET,
	/**
	 * Calibration target. This will be used by the internal chip's
	 * algorithms to calibrate itself on a certain axis, or all of them.
	 */
	ACTUATOR_ATTR_CALIB_TARGET,
	/** Configure the operating modes of an actuator. */
	ACTUATOR_ATTR_CONFIGURATION,
	/** Set a calibration value needed by an actuator. */
	ACTUATOR_ATTR_CALIBRATION,
	/** Enable/disable actuator features */
	ACTUATOR_ATTR_FEATURE_MASK,
	/** Alert threshold or alert enable/disable */
	ACTUATOR_ATTR_ALERT,

	/**
	 * Number of all common actuator attributes.
	 */
	ACTUATOR_ATTR_COMMON_COUNT,

	/**
	 * This and higher values are actuator specific.
	 * Refer to the actuator header file.
	 */
	ACTUATOR_ATTR_PRIV_START = ACTUATOR_ATTR_COMMON_COUNT,
	/**
	 * Maximum value describing an actuator attribute type.
	 */
	ACTUATOR_ATTR_MAX = INT16_MAX,
};

/**
 * @brief Representation of an actuator write-/read-out value.
 *
 * The value is represented as having an integer and a fractional part,
 * and can be obtained using the formula val1 + val2 * 10^(-6). Negative
 * values also adhere to the above formula, but may need special attention.
 * Here are some examples of the value representation:
 *
 *      0.5: val1 =  0, val2 =  500000
 *     -0.5: val1 =  0, val2 = -500000
 *     -1.0: val1 = -1, val2 =  0
 *     -1.5: val1 = -1, val2 = -500000
 */
struct actuator_value {
	/** Integer part of the value. */
	int32_t val1;
	/** Fractional part of the value (in one-millionth parts). */
	int32_t val2;
};

/**
 * @brief Actuator trigger types.
 */
enum actuator_trigger_type {
	/**
	 * Maximum value describing an actuator trigger type.
	 */
	ACTUATOR_TRIG_MAX = INT16_MAX,
};

/**
 * @brief Actuator trigger spec.
 */
struct actuator_trigger {
	/** Trigger type. */
	enum actuator_trigger_type type;
	/** Channel the trigger is set on. */
	enum actuator_channel chan;
};

/**
 * @typedef actuator_attr_set_t
 * @brief Callback API upon setting a actuator's attributes
 *
 * See actuator_attr_set() for argument description
 */
typedef int (*actuator_attr_set_t)(const struct device *dev,
				   enum actuator_channel chan,
				   enum actuator_attribute attr,
				   const struct actuator_value *val);

/**
 * @typedef actuator_attr_get_t
 * @brief Callback API upon getting a actuator's attributes
 *
 * See actuator_attr_get() for argument description
 */
typedef int (*actuator_attr_get_t)(const struct device *dev,
				   enum actuator_channel chan,
				   enum actuator_attribute attr,
				   struct actuator_value *val);

/**
 * @typedef actuator_trigger_handler_t
 * @brief Callback API upon firing of a trigger
 *
 * @param dev Pointer to the actuator device
 * @param trigger The trigger
 */
typedef void (*actuator_trigger_handler_t)(const struct device *dev,
					   const struct actuator_trigger *trigger);

/**
 * @typedef actuator_trigger_set_t
 * @brief Callback API for setting a actuator's trigger and handler
 *
 * See actuator_trigger_set() for argument description
 */
typedef int (*actuator_trigger_set_t)(const struct device *dev,
				      const struct actuator_trigger *trig,
				      actuator_trigger_handler_t handler);

__subsystem struct actuator_driver_api {
	actuator_attr_set_t attr_set;
	actuator_attr_get_t attr_get;
	actuator_trigger_set_t trigger_set;
};

/**
 * @brief Set an attribute for an actuator
 *
 * @param dev Pointer to the actuator device
 * @param chan The channel the attribute belongs to, if any.  Some
 * attributes may only be set for all channels of a device, depending on
 * device capabilities.
 * @param attr The attribute to set
 * @param val The value to set the attribute to
 *
 * @return 0 if successful, negative errno code if failure.
 */
__syscall int actuator_attr_set(const struct device *dev,
			        enum actuator_channel chan,
			        enum actuator_attribute attr,
			        const struct actuator_value *val);

static inline int z_impl_actuator_attr_set(const struct device *dev,
					   enum actuator_channel chan,
					   enum actuator_attribute attr,
					   const struct actuator_value *val)
{
	const struct actuator_driver_api *api =
		(const struct actuator_driver_api *)dev->api;

	if (api->attr_set == NULL) {
		return -ENOSYS;
	}

	return api->attr_set(dev, chan, attr, val);
}

/**
 * @brief Get an attribute for an actuator
 *
 * @param dev Pointer to the actuator device
 * @param chan The channel the attribute belongs to, if any.  Some
 * attributes may only be set for all channels of a device, depending on
 * device capabilities.
 * @param attr The attribute to get
 * @param val Pointer to where to store the attribute
 *
 * @return 0 if successful, negative errno code if failure.
 */
__syscall int actuator_attr_get(const struct device *dev,
			        enum actuator_channel chan,
			        enum actuator_attribute attr,
			        struct actuator_value *val);

static inline int z_impl_actuator_attr_get(const struct device *dev,
					   enum actuator_channel chan,
					   enum actuator_attribute attr,
					   struct actuator_value *val)
{
	const struct actuator_driver_api *api =
		(const struct actuator_driver_api *)dev->api;

	if (api->attr_get == NULL) {
		return -ENOSYS;
	}

	return api->attr_get(dev, chan, attr, val);
}

/**
 * @brief Activate a actuator's trigger and set the trigger handler
 *
 * The handler will be called from a thread, so I2C or SPI operations are
 * safe.  However, the thread's stack is limited and defined by the
 * driver.  It is currently up to the caller to ensure that the handler
 * does not overflow the stack.
 *
 * @funcprops \supervisor
 *
 * @param dev Pointer to the actuator device
 * @param trig The trigger to activate
 * @param handler The function that should be called when the trigger
 * fires
 *
 * @return 0 if successful, negative errno code if failure.
 */
static inline int actuator_trigger_set(const struct device *dev,
				     const struct actuator_trigger *trig,
				     actuator_trigger_handler_t handler)
{
	const struct actuator_driver_api *api =
		(const struct actuator_driver_api *)dev->api;

	if (api->trigger_set == NULL) {
		return -ENOSYS;
	}

	return api->trigger_set(dev, trig, handler);
}

/**
 * @brief Helper function for converting struct actuator_value to double.
 *
 * @param val A pointer to a actuator_value struct.
 * @return The converted value.
 */
static inline double actuator_value_to_double(const struct actuator_value *val)
{
	return (double)val->val1 + (double)val->val2 / 1000000;
}

#ifdef CONFIG_BRIDLE_ACTUATOR_INFO

struct actuator_info {
	const struct device *dev;
	const char *vendor;
	const char *model;
	const char *friendly_name;
};

#define BRIDLE_ACTUATOR_INFO_INITIALIZER(				\
				_dev, _vendor, _model, _friendly_name)	\
	{								\
		.dev = _dev,						\
		.vendor = _vendor,					\
		.model = _model,					\
		.friendly_name = _friendly_name,			\
	}

#define BRIDLE_ACTUATOR_INFO_DEFINE(name, ...)				\
	static const STRUCT_SECTION_ITERABLE(actuator_info, name) =	\
		BRIDLE_ACTUATOR_INFO_INITIALIZER(__VA_ARGS__)

#define BRIDLE_ACTUATOR_INFO_DT_NAME(node_id)				\
	_CONCAT(__actuator_info, DEVICE_DT_NAME_GET(node_id))

#define BRIDLE_ACTUATOR_INFO_DT_DEFINE(node_id)				\
	BRIDLE_ACTUATOR_INFO_DEFINE(					\
			BRIDLE_ACTUATOR_INFO_DT_NAME(node_id),		\
			DEVICE_DT_GET(node_id),				\
			DT_NODE_VENDOR_OR(node_id, NULL),		\
			DT_NODE_MODEL_OR(node_id, NULL),		\
			DT_PROP_OR(node_id, friendly_name, NULL))	\

#else

#define BRIDLE_ACTUATOR_INFO_DEFINE(name, ...)
#define BRIDLE_ACTUATOR_INFO_DT_DEFINE(node_id)

#endif /* CONFIG_BRIDLE_ACTUATOR_INFO */

/**
 * @brief Like DEVICE_DT_DEFINE() with actuator specifics.
 *
 * @details Defines a device which implements the actuator API. May define an
 * element in the actuator info iterable section used to enumerate all actuator
 * devices.
 *
 * @param node_id The devicetree node identifier.
 *
 * @param init_fn Name of the init function of the driver.
 *
 * @param pm_device PM device resources reference (NULL if device does not use
 * PM).
 *
 * @param data_ptr Pointer to the device's private data.
 *
 * @param cfg_ptr The address to the structure containing the configuration
 * information for this instance of the driver.
 *
 * @param level The initialization level. See SYS_INIT() for details.
 *
 * @param prio Priority within the selected initialization level. See
 * SYS_INIT() for details.
 *
 * @param api_ptr Provides an initial pointer to the API function struct used
 * by the driver. Can be NULL.
 */
#define BRIDLE_ACTUATOR_DEVICE_DT_DEFINE(node_id, init_fn, pm_device,	\
				data_ptr, cfg_ptr, level, prio,		\
				api_ptr, ...)				\
	DEVICE_DT_DEFINE(node_id, init_fn, pm_device,			\
			 data_ptr, cfg_ptr, level, prio,		\
			 api_ptr, __VA_ARGS__);				\
									\
	BRIDLE_ACTUATOR_INFO_DT_DEFINE(node_id);

/**
 * @brief Like BRIDLE_ACTUATOR_DEVICE_DT_DEFINE() for an instance
 * of a DT_DRV_COMPAT compatible
 *
 * @param inst instance number. This is replaced by <tt>DT_DRV_COMPAT(inst)</tt>
 * in the call to BRIDLE_ACTUATOR_DEVICE_DT_DEFINE().
 *
 * @param ... other parameters as expected by BRIDLE_ACTUATOR_DEVICE_DT_DEFINE().
 */
#define BRIDLE_ACTUATOR_DEVICE_DT_INST_DEFINE(inst, ...)		\
	BRIDLE_ACTUATOR_DEVICE_DT_DEFINE(DT_DRV_INST(inst), __VA_ARGS__)

#ifdef __cplusplus
}
#endif

/**
 * @}
 */

#include <syscalls/actuator.h>

#endif /* BRIDLE_INCLUDE_DRIVERS_ACTUATOR_H_ */
