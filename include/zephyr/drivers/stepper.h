/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 Carl Zeiss Meditec AG
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Public Stepper Motor API
 */

#ifndef ZEPHYR_INCLUDE_DRIVERS_STEPPER_H_
#define ZEPHYR_INCLUDE_DRIVERS_STEPPER_H_

#include <stdlib.h>
#include <errno.h>

#include <zephyr/sys/__assert.h>
#include <zephyr/sys/atomic.h>
#include <zephyr/sys/iterable_sections.h>

#include <zephyr/types.h>
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/dt-bindings/stepper/stepper.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Stepper Motor Interface
 * @defgroup stepper_interface Stepper Motor Interface
 * @since 4.0
 * @version 0.1.0
 * @ingroup io_interfaces
 * @{
 *
 * @details Stepper motors are manufactured with two coils of wire, resulting
 * in one winding per phase. By alternating the power between coils, as well
 * as the direction of the current, the motor is rotated. The stepper motor
 * can reverse the direction of rotation simply by reversing this sequence.
 * The wiring of the two phases, or more precisely the start and end of the
 * two coils, to the stepper motor driver determines the default direction of
 * rotation. Mostly this is "forward" or "right" direction for "positive" and
 * "backward" or "left" direction for "negative".
 *
 * Depending on the number of these sequential individual steps and the amount
 * with which they occur in relation to time, a stepper motor can be operated
 * either for precise positioning in the "positioning mode" or highly constant
 * rotational speed in the "velocity mode", also often called "free running":
 *
 * - @see STEPPER_OP_MODE_POSITION for "positioning mode"
 * - @see STEPPER_OP_MODE_VELOCITY for "velocity mode" (free running)
 *
 * The final direction of rotation is determined by a "positive" or "negative"
 * value. In the case of "positioning mode" by "microsteps" as the position and
 * in "velocity mode" by the "rotational speed" as the velocity.
 *
 * The terms "position" and "microsteps" are ambivalent, unitless and often
 * have the same meaning, depending on the context in which they are used. In
 * "positioning mode", the value of the microsteps can be designated only as
 * "relative". Relative microsteps move the stepper motor away from the current
 * (stepper motor owned) absolute position accordingly.
 *
 * In "velocity mode", the value of velocity, the rotational speed, is defined
 * as "microsteps per second" and can be designated only as "absolute".
 * Absolute velocity, in other words a "new velocity", change the rotational
 * speed exactly.
 *
 * @note In "velocity mode", the value of velocity is defined as "microsteps
 * per second" based to "full-stepping" (internal multiplicated by current
 * microstep resolution). Common values are:
 *
 * -   < 10 (extremely slow),
 * -    100 (very slow),
 * -    500 (fast),
 * -   1000 (very fast),
 * - > 1500 (extremely fast).
 *
 * These are only example values for full steps, where the resolution of
 * microsteps is defined as 1 (no multiplications). Depending on the common
 * step angles, usage of microstep resolution greater than 1 and whether
 * gears also play a role, these values can be completely different.
 *
 * @note When a stepper motor becomes engaged in software, and current is
 * applied to the coils, it may abruptly "snap" to the position that the
 * rotor is being held at.
 *
 */

/**
 * @brief Representation of a stepper action.
 *
 * @details The action structure represents all values that are
 * required for general or special actions that can be executed by stepper
 * motors.
 */
struct stepper_action {
	/** Operation mode and microstep resolution flags. */
	uint32_t flags;
	/** Microsteps, velocity, or acceleratio.n */
	int32_t value;
};

/**
 * @name Stepper motor operation mode flags.
 * @{
 *
 * @note The acceleration mode is not (yet) supported. It is unclear whether
 * this makes sense at all, as further limit value considerations such as
 * reaching the maximum speed and the associated behavior would have to be
 * implemented. However, these are already tasks of a stepper motor control
 * layer and should not be the task of the driver layer. However, it is
 * possible that the driver layer can play a mediating role here. Then
 * at least this behavior should be implemented.
 */

/** Enable positioning mode (forward or backward) by microsteps. */
#define STEPPER_OP_MODE_POSITION	(1U << 16)

/** Enable free running mode (forward or backward) by velocity. */
#define STEPPER_OP_MODE_VELOCITY	(1U << 17)

/** Enable accelerating mode (forward or backward) by acceleration. */
#define STEPPER_OP_MODE_ACCELERATION	(1U << 18)

/** @} */

/**
 * @cond INTERNAL_HIDDEN
 *
 * For internal driver use only, skip these in public documentation.
 */

/** Bit mask for operation mode access in flags. */
#define STEPPER_OP_MODE_MASK		(STEPPER_OP_MODE_POSITION	| \
					 STEPPER_OP_MODE_VELOCITY	| \
					 STEPPER_OP_MODE_ACCELERATION)

/** Get stepper motor operational mode. */
#define STEPPER_OP_MODE_GET(_flags_)	((_flags_) & (STEPPER_OP_MODE_MASK))

/** Bit mask for microstep resolution access in flags. */
#define STEPPER_USTEP_RES_MASK		(STEPPER_USTEP_RES_1		| \
					 STEPPER_USTEP_RES_2		| \
					 STEPPER_USTEP_RES_4		| \
					 STEPPER_USTEP_RES_8		| \
					 STEPPER_USTEP_RES_16		| \
					 STEPPER_USTEP_RES_32		| \
					 STEPPER_USTEP_RES_64		| \
					 STEPPER_USTEP_RES_128		| \
					 STEPPER_USTEP_RES_256)

/** Get stepper motor microstep resolution. */
#define STEPPER_USTEP_RES_GET(_flags_)	((_flags_) & (STEPPER_USTEP_RES_MASK))

/**
 * @typedef stepper_api_on
 * @brief API for enabling the stepper motor.
 *
 * @see stepper_on() for argument descriptions.
 */
typedef int (*stepper_api_on)(const struct device *dev, const uint8_t motor);

/**
 * @typedef stepper_api_off
 * @brief API for disabling the stepper motor.
 *
 * @see stepper_off() for argument descriptions.
 */
typedef int (*stepper_api_off)(const struct device *dev, const uint8_t motor);

/**
 * @typedef stepper_api_move
 * @brief API for movement according to the provided action.
 *
 * @see stepper_move() for argument descriptions.
 */
typedef int (*stepper_api_move)(const struct device *dev, const uint8_t motor,
				const struct stepper_action *action);

/**
 * @brief Stepper Motor API.
 *
 * @details This is the mandatory API any stepper motor device driver needs
 * to expose with exception of:
 *   TBD() are only required for TBD drivers (TODO)
 */
__subsystem struct stepper_api {
	stepper_api_on on;
	stepper_api_off off;
	stepper_api_move move;
};

#define STEPPER_BUILD_ASSERT_DT_PROP_LT(node_id, prop, val, MSG...)	\
	BUILD_ASSERT(DT_PROP(node_id, prop) < (val), "" MSG)
#define STEPPER_BUILD_ASSERT_DT_INST_PROP_LT(inst, ...)			\
	STEPPER_BUILD_ASSERT_DT_PROP_LT(DT_DRV_INST(inst), __VA_ARGS__)

#define STEPPER_BUILD_ASSERT_DT_PROP_EQ(node_id, prop, val, MSG...)	\
	BUILD_ASSERT(DT_PROP(node_id, prop) = (val), "" MSG)
#define STEPPER_BUILD_ASSERT_DT_INST_PROP_EQ(inst, ...)			\
	STEPPER_BUILD_ASSERT_DT_PROP_EQ(DT_DRV_INST(inst), __VA_ARGS__)

#define STEPPER_BUILD_ASSERT_DT_PROP_GT(node_id, prop, val, MSG...)	\
	BUILD_ASSERT(DT_PROP(node_id, prop) > (val), "" MSG)
#define STEPPER_BUILD_ASSERT_DT_INST_PROP_GT(inst, ...)			\
	STEPPER_BUILD_ASSERT_DT_PROP_GT(DT_DRV_INST(inst), __VA_ARGS__)

/** @endcond */

/**
 * @brief Stepper motor event types.
 */
enum stepper_event_type {
        /** Device suspended (or sleep) event. */
        STEPPER_EVT_SUSPEND,
        /** Device reset detected. */
        STEPPER_EVT_RESET,
        /** Device fault detected. */
        STEPPER_EVT_FAULT,
        /**
         * Non-recoverable error event, requires attention from higher
         * levels or application.
         */
        STEPPER_EVT_ERROR,
};

/**
 * @brief Stepper motor event.
 *
 * @details: Common structure for all events that originate from a stepper motor
 * driver and are passed to higher layers using (TODO/TBD: message queue and) a
 * callback (stepper_event_cb_t) provided by higher layers during (TODO/TBD:
 * driver initialization).
 */
struct stepper_event {
	/** Event type. */
	enum stepper_event_type type;
	union {
		/** Event value. */
		uint32_t value;
		/** Event status value, if any. */
		int status;
	};
	/** Stepper motor device driver instance. */
	const struct device *dev;
	/** Stepper motor number. */
	const uint8_t motor;
};

/**
 * @typedef stepper_event_cb_t
 * @brief Callback to submit stepper motor event to higher layer.
 *
 * @details At the higher level, the event is to be inserted into (TODO/TBD:
 * a message queue). (TBD) Maybe it is better to provide a pointer to k_msgq
 * passed during initialization.
 *
 * @param[in] dev       Stepper motor device driver instance.
 * @param[in] event     Pointer to the stepper motor event description.
 *
 * @return 0 on success, all other values should be treated as error.
 */
typedef int (*stepper_event_cb_t)(const struct device *dev,
				  const struct stepper_event *const event);

/** @brief Structure holding stepper motor device driver capabilities. */
struct stepper_capabilities {
	/** Possible number of motors in parallel operation.
	const uint8_t motors; */
	/** Possible operation mode and microstep resolution. */
	const uint32_t flags;
	/** Number of full-steps for one full turn. */
	const uint32_t fs_per_turn;
	/** Highest full-step rotational speed. */
	const uint32_t fs_max_speed;
};

/**
 * @brief Initialize a struct stepper_capabilities from devicetree.
 *
 * @details This helper allows drivers to initializes an element in the
 * stepper motor device driver capability structure via devicetree.
 *
 * @note The acceleration operating mode that is not (yet) supported is
 * therefore filtered out, @see STEPPER_OP_MODE_ACCELERATION.
 *
 * @param node_id   Devicetree node identifier for the stepper motor
 *                  device whose struct stepper_capabilities to create
 *                  an initializer for.
 * @param flags     The desired flags field in struct stepper_capabilities.
 */
#define STEPPER_CAPS_DT(node_id, flags_)				\
	{								\
		.flags = (((STEPPER_OP_MODE_GET((flags_)) |		\
			    STEPPER_USTEP_RES_GET((flags_))		\
			   ) & GENMASK(31, 0)				\
			  ) & ~STEPPER_OP_MODE_ACCELERATION),		\
		.fs_per_turn = DT_PROP(node_id, fs_per_turn),		\
		.fs_max_speed = DT_PROP(node_id, fs_max_speed),		\
	}

/**
 * @brief Initialize a struct stepper_capabilities from devicetree instance.
 *
 * @details This helper initializes an element for the stepper motor device
 * driver capability structure from a devicetree instance. It is equivalent
 * to @see STEPPER_CAPS_DATA_DT(DT_DRV_INST(inst)).
 *
 * @param inst      Instance number to initialize capability from.
 * @param flags     The desired flags field in struct stepper_capabilities.
 */
#define STEPPER_CAPS_DT_INST(inst, flags_)				\
	STEPPER_CAPS_DT(DT_DRV_INST(inst), flags_)

/**
 * @brief Defines and initialize a struct stepper_capabilities from a single
 *        devicetree instance.
 *
 * @details This helper defines and initializes a stepper motor device driver
 * capability structure from a devicetree instance.
 *
 * @param inst      Instance number to initialize capability from.
 * @param caps      The desired instance name of the struct stepper_capabilities.
 * @param flags     The desired flags field in struct stepper_capabilities.
 */
#define STEPPER_CAPS_DT_INST_DEFINE(inst, caps_, flags_, ...)		\
									\
	STEPPER_BUILD_ASSERT_DT_INST_PROP_GT(inst, fs_per_turn, 0,	\
		"Full-steps per full turn must be greater than zero.");	\
									\
	STEPPER_BUILD_ASSERT_DT_INST_PROP_GT(inst, fs_max_speed, 0,	\
		"Maximum rotational speed must be greater than zero.");	\
									\
	static const struct stepper_capabilities caps_##inst[] = {	\
		STEPPER_CAPS_DT_INST(inst, (flags_))			\
	};

/**
 * @brief Defines and initialize a struct stepper_capabilities from multiple
 *        devicetree instances (child nodes).
 *
 * @details This helper defines and initializes a stepper motor device driver
 * capability structure from a devicetree instance.
 *
 * @param inst      Instance number to initialize capability from.
 * @param caps      The desired instance name of the struct stepper_capabilities.
 * @param flags     The desired flags field in struct stepper_capabilities.
 */
#define STEPPER_CAPS_CHILDS_DT_INST_DEFINE(inst, caps_, flags_, ...)	\
									\
	DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP_VARGS(inst,		\
		STEPPER_BUILD_ASSERT_DT_PROP_GT, (;), fs_per_turn, 0,	\
		"Full-steps per full turn must be greater than zero.");	\
									\
	DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP_VARGS(inst,		\
		STEPPER_BUILD_ASSERT_DT_PROP_GT, (;), fs_max_speed, 0,	\
		"Maximum rotational speed must be greater than zero.");	\
									\
	static const struct stepper_capabilities caps_##inst[] = {	\
		DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP_VARGS(inst,	\
					STEPPER_CAPS_DT, (,), (flags_))	\
	};

/**
 * @brief Common stepper motor driver data structure.
 *
 * @details Mandatory structure for each stepper motor device driver.
 * To be implemented as device's private data (device->data).
 *
 * @note The "const" qualifiers should only be removed when there is
 * a low level driver that has to dynamically adapt its own capabilities
 * at runtime due to changing reality. Suitable internal API functions
 * must then also be added to stepper_common.h as inline, more complex
 * functions in to stepper_common.c not as inline.
 */
struct stepper_data {
	/** Number of managed stepper motors and thus also capabilities. */
	const size_t num_motor;
	/** Stepper motor driver capabilities. */
	const struct stepper_capabilities *const caps;
	/** Stepper motor driver access mutex. */
	struct k_mutex mutex;
	/** TODO: Callback to submit an stepper motor event to upper layer. */
	stepper_event_cb_t event_cb;
	/** TODO: Stepper motor driver status. */
	atomic_t status;
	/** Stepper motor driver private data. */
	void *priv;
};

/**
 * @brief Initialize a struct stepper_data from devicetree instance.
 *
 * @details This helper initializes a stepper motor device driver data
 * structure from a devicetree instance.
 *
 * @param inst      Instance number to initialize capability from.
 * @param data      The desired instance name of the struct stepper_data.
 * @param priv      The desired private data pointer in struct stepper_data.
 * @param motors    The desired number of motors in struct stepper_capabilities.
 * @param flags     The desired flags field in struct stepper_capabilities.
 */
#define STEPPER_DATA_DT_INST_INITIALIZER(inst, data_, priv_, caps_, ...)\
	{								\
		.num_motor = ARRAY_SIZE((caps_)),			\
		.caps = (caps_),					\
		.mutex = Z_MUTEX_INITIALIZER((data_).mutex),		\
		.priv = &(priv_),					\
	}

/**
 * @brief Defines and initialize a struct stepper_data from devicetree instance.
 *
 * @details This helper defines and initializes a stepper motor device driver
 * data structure from a devicetree instance.
 *
 * @todo We are missing a CPP macro like DT_HAS_CHILD() to identify the
 * presence of child nodes. Therefore, only an indirect test for the
 * property "fs-per-turn" is performed in COND_CODE_1. This indirect
 * check works because this property is defined as mandatory and required.
 * However, there is an extremely high risk that changes in the Devicetree
 * bindings will cause this special API macro to suddenly, unexpectedly
 * and almost obviously no longer work as intended!
 *
 * @param inst      Instance number to initialize capability from.
 * @param data      The desired instance name of the struct stepper_data.
 * @param priv      The desired private data pointer in struct stepper_data.
 * @param caps      The desired instance name of the struct stepper_capabilities.
 * @param flags     The desired flags field in struct stepper_capabilities.
 * @param ...       Other parameters as may expected by
 *                  STEPPER_DATA_DT_INST_INITIALIZER().
 */
#define STEPPER_DATA_DT_INST_DEFINE(inst, data_, priv_,			\
					  caps_, flags_, ...)		\
									\
	BUILD_ASSERT(STEPPER_OP_MODE_GET((flags_)) != 0,		\
		"At least one operation mode must be set.");		\
									\
	BUILD_ASSERT(STEPPER_USTEP_RES_GET((flags_)) != 0,		\
		"At least one microstep resolution must be set.");	\
									\
	COND_CODE_1(DT_INST_NODE_HAS_PROP(inst, fs_per_turn),		\
		(STEPPER_CAPS_DT_INST_DEFINE(inst, caps_, (flags_))),	\
		(STEPPER_CAPS_CHILDS_DT_INST_DEFINE(inst, caps_,	\
							  (flags_))))	\
									\
	static struct stepper_data data_##inst				\
		= STEPPER_DATA_DT_INST_INITIALIZER(inst,		\
			data_##inst, priv_##inst, caps_##inst, __VA_ARGS__)

/**
 * @brief Get stepper motor driver capabilities
 *
 * Obtain the capabilities of the stepper motor such as operation mode,
 * microstep resolution, number of full-steps for one full turn, highest
 * full-step rotational speed, and more.
 *
 * @param[in] dev      Stepper motor device driver instance.
 *
 * @return Stepper motor device driver capabilities.
 */
static inline const struct stepper_capabilities *const stepper_caps(
					const struct device *const dev)
{
	const struct stepper_data *const data = dev->data;

	return data->caps;
}

/* TODO: static inline bool stepper_is_initialized(const struct device *dev) */
/* TODO: static inline bool stepper_is_enabled(const struct device *dev) */
/* TODO: static inline bool stepper_is_suspended(const struct device *dev) */
/* TODO: int stepper_init(const struct device *dev, stepper_event_cb_t event_cb); */
/* TODO: int stepper_enable(const struct device *dev); */
/* TODO: int stepper_disable(const struct device *dev); */
/* TODO: int stepper_shutdown(const struct device *dev); */

/**
 * @brief API for enabling the stepper motor.
 *
 * @details This routine turns on the hardware components that supply
 * the coils of the stepper motor with electrical current.
 *
 * @param[in] dev       Stepper motor device driver instance.
 * @param[in] motor     Stepper motor number.
 *
 * @retval 0            If successful.
 * @retval -ENXIO       If motor is invalid or exceeds hardware capabilities.
 * @return -errno code  on other failure.
 */
__syscall int stepper_on(const struct device *dev, const uint8_t motor);

static inline int z_impl_stepper_on(const struct device *dev, const uint8_t motor)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;
	const struct stepper_data *data = (const struct stepper_data *)dev->data;

	__ASSERT_NO_MSG(api != NULL);
	__ASSERT_NO_MSG(api->on != NULL);
	__ASSERT_NO_MSG(data != NULL);

	if (!IN_RANGE(motor, 0, data->num_motor - 1)) {
		/* incapable motor number */
		return -ENXIO;
	}

	return api->on(dev, motor);
}

/**
 * @brief API for disabling the stepper motor.
 *
 * @details This routine turns off the hardware components that supply
 * the coils of the stepper motor with electrical current.
 *
 * @param[in] dev       Stepper motor device driver instance.
 * @param[in] motor     Stepper motor number.
 *
 * @retval 0            If successful.
 * @retval -ENXIO       If motor is invalid or exceeds hardware capabilities.
 * @return -errno code  on other failure.
 */
__syscall int stepper_off(const struct device *dev, const uint8_t motor);

static inline int z_impl_stepper_off(const struct device *dev, const uint8_t motor)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;
	const struct stepper_data *data = (const struct stepper_data *)dev->data;

	__ASSERT_NO_MSG(api != NULL);
	__ASSERT_NO_MSG(api->off != NULL);
	__ASSERT_NO_MSG(data != NULL);

	if (!IN_RANGE(motor, 0, data->num_motor - 1)) {
		/* Invalid motor number */
		return -ENXIO;
	}

	return api->off(dev, motor);
}

/**
 * @brief API for flag dependent movement.
 *
 * @details Set the microsteps to be moved from the current absolut position,
 * a.k.a. relative position movement or set the microsteps per second, the
 * absolute velocity, to be used for continuous movement, a.k.a. free running.
 *
 * - @see STEPPER_OP_MODE_POSITION for "positioning mode"
 * - @see STEPPER_OP_MODE_VELOCITY for "velocity mode" (free running)
 *
 * @note The accelerating mode is not (yet) supported.
 *       @see STEPPER_OP_MODE_ACCELERATION for details.
 *
 * @param[in] dev       Stepper motor device driver instance.
 * @param[in] motor     Stepper motor number.
 * @param[in] action    Pointer to the stepper motor action description.
 *
 * @retval 0            If successful.
 * @retval -EIO         If internal I/O operation failure.
 * @retval -ENXIO       If motor is invalid or exceeds hardware capabilities.
 * @retval -EINVAL      If action is invalid or exceeds hardware capabilities.
 * @retval -ENOTSUP     If action or operation mode is not supported.
 * @return -errno code  on other failure.
 */
__syscall int stepper_move(const struct device *dev, const uint8_t motor,
			   const struct stepper_action *action);

static inline int z_impl_stepper_move(const struct device *dev, const uint8_t motor,
				      const struct stepper_action *action)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;
	const struct stepper_data *data = (const struct stepper_data *)dev->data;
	const struct stepper_capabilities *caps = &data->caps[motor];

	__ASSERT_NO_MSG(api != NULL);
	__ASSERT_NO_MSG(api->move != NULL);
	__ASSERT_NO_MSG(data != NULL);

	if (!IN_RANGE(motor, 0, data->num_motor - 1)) {
		/* Invalid motor number */
		return -ENXIO;
	}

	if (STEPPER_OP_MODE_GET(action->flags) == 0) {
		/* No operation mode set */
		return -EINVAL;
	}

	if (STEPPER_USTEP_RES_GET(action->flags) == 0) {
		/* No microstep resolution set */
		return -EINVAL;
	}

	if ((STEPPER_USTEP_RES_GET(action->flags) &
	     STEPPER_USTEP_RES_GET(caps->flags)) == 0) {
		/* Invalid microstep resolutions set */
		return -EINVAL;
	}

	if (!IS_POWER_OF_TWO(STEPPER_USTEP_RES_GET(action->flags))) {
		/* Multiple microstep resolutions set */
		return -EINVAL;
	}

	if ((STEPPER_OP_MODE_GET(action->flags) == STEPPER_OP_MODE_POSITION) &&
	    (!IN_RANGE(labs(action->value), 1, UINT32_MAX))) {
		/* Invalid microstep move (relative position) set */
		return -EINVAL;
	}

	if ((STEPPER_OP_MODE_GET(action->flags) == STEPPER_OP_MODE_VELOCITY) &&
	    (!IN_RANGE(labs(action->value), 0, caps->fs_max_speed))) {
		/* Invalid rotational speed (absolute velocity) set */
		return -EINVAL;
	}

	if (STEPPER_OP_MODE_GET(action->flags) == STEPPER_OP_MODE_ACCELERATION) {
		/* TBD: accelerating mode not (yet) supported */
		return -ENOTSUP;
	}

	return api->move(dev, motor, action);
}

#ifdef CONFIG_STEPPER_INFO

/** @brief Structure holding stepper motor information. */
struct stepper_info {
	/** Stepper motor device driver instance. */
	const struct device *dev;
	/** Stepper motor number. */
	const uint8_t motor;
	/** Vendor name from compatibility property. */
	const char *vendor;
	/** Model name from compatibility property. */
	const char *model;
	/** Friendly name. */
	const char *friendly_name;
};

/** @cond INTERNAL_HIDDEN */

#define STEPPER_INFO_INITIALIZER(_dev, _motor, _vendor, _model,		\
							_friendly_name)	\
	{								\
		.dev = _dev,						\
		.motor = _motor,					\
		.vendor = _vendor,					\
		.model = _model,					\
		.friendly_name = _friendly_name,			\
	}

#define STEPPER_INFO_DEFINE(name, ...)					\
	static const STRUCT_SECTION_ITERABLE(stepper_info, name) =	\
		STEPPER_INFO_INITIALIZER(__VA_ARGS__)

#define STEPPER_INFO_DT_NAME(node_id)					\
	_CONCAT(__stepper_info, DEVICE_DT_NAME_GET(node_id))

#define STEPPER_INFO_DT_DEFINE(node_id)					\
	STEPPER_INFO_DEFINE(STEPPER_INFO_DT_NAME(node_id),		\
			    DEVICE_DT_GET(node_id),			\
			    (0) /* no childs, single motor instance */,	\
			    DT_NODE_VENDOR_OR(node_id, NULL),		\
			    DT_NODE_MODEL_OR(node_id, NULL),		\
			    DT_PROP_OR(node_id, friendly_name, NULL))	\

#define STEPPER_INFO_DT_CHILD_DEFINE(node_id)				\
	STEPPER_INFO_DEFINE(STEPPER_INFO_DT_NAME(node_id),		\
			    DEVICE_DT_GET(DT_PARENT(node_id)),		\
			    DT_NODE_CHILD_IDX(node_id),			\
			    DT_NODE_VENDOR_OR(node_id, NULL),		\
			    DT_NODE_MODEL_OR(node_id, NULL),		\
			    DT_PROP_OR(node_id, friendly_name, NULL))	\

#define STEPPER_INFO_DT_FOREACH_CHILD_DEFINE(node_id)			\
	DT_FOREACH_CHILD_STATUS_OKAY_SEP(				\
			node_id, STEPPER_INFO_DT_CHILD_DEFINE, (;))

/** @endcond */

#else

/** @cond INTERNAL_HIDDEN */

#define STEPPER_INFO_DEFINE(name, ...)
#define STEPPER_INFO_DT_DEFINE(node_id)
#define STEPPER_INFO_DT_FOREACH_CHILD_DEFINE(node_id)

/** @endcond */

#endif /* CONFIG_STEPPER_INFO */

/**
 * @brief Like DEVICE_DT_DEFINE() with stepper motor specifics.
 *
 * @details Defines a device which implements the stepper motor API. May
 * define an element in the stepper motor info iterable section used to
 * enumerate all stepper motor devices depending on
 * @kconfig{CONFIG_STEPPER_INFO}.
 *
 * @todo We are missing a CPP macro like DT_HAS_CHILD() to identify the
 * presence of child nodes. Therefore, only an indirect test for the
 * property "fs-per-turn" is performed in COND_CODE_1. This indirect
 * check works because this property is defined as mandatory and required.
 * However, there is an extremely high risk that changes in the Devicetree
 * bindings will cause this special API macro to suddenly, unexpectedly
 * and almost obviously no longer work as intended!
 *
 * @param node_id The devicetree node identifier.
 *
 * @param init_fn Name of the init function of the driver.
 *
 * @param pm_device PM device resources reference (NULL if device does not
 * use PM).
 *
 * @param data_ptr Pointer to the device's private data.
 *
 * @param cfg_ptr The address to the structure containing the configuration
 * information for this instance of the driver.
 *
 * @param level The initialization level. See SYS_INIT() for details.
 *
 * @param prio Priority within the selected initialization level.
 * See SYS_INIT() for details.
 *
 * @param api_ptr Provides an initial pointer to the API function struct
 * used by the driver. Can be NULL.
									\
 */
#define STEPPER_DEVICE_DT_DEFINE(node_id, init_fn, pm_device,		\
				data_ptr, cfg_ptr, level, prio,		\
				api_ptr, ...)				\
									\
	DEVICE_DT_DEFINE(node_id, init_fn, pm_device,			\
			 data_ptr, cfg_ptr, level, prio,		\
			 api_ptr, __VA_ARGS__);				\
									\
	COND_CODE_1(DT_NODE_HAS_PROP(node_id, fs_per_turn),		\
		(STEPPER_INFO_DT_DEFINE(node_id)),			\
		(STEPPER_INFO_DT_FOREACH_CHILD_DEFINE(node_id)));

/**
 * @brief Like STEPPER_DEVICE_DT_DEFINE() for an instance of a DT_DRV_INST
 * compatible
 *
 * @param inst instance number. This is replaced by
 * <tt>DT_DRV_INST(inst)</tt> in the call to STEPPER_DEVICE_DT_DEFINE().
 *
 * @param ... other parameters as expected by STEPPER_DEVICE_DT_DEFINE().
 */
#define STEPPER_DEVICE_DT_INST_DEFINE(inst, ...)			\
	STEPPER_DEVICE_DT_DEFINE(DT_DRV_INST(inst), __VA_ARGS__)

/**
 * @}
 */

#ifdef __cplusplus
}
#endif

#include <zephyr/syscalls/stepper.h>

#endif /* ZEPHYR_INCLUDE_DRIVERS_STEPPER_H_ */
