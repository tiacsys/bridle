/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 Carl Zeiss Meditec AG
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Public Stepper Motor Controller API
 *
 */

#ifndef ZEPHYR_INCLUDE_DRIVERS_STEPPER_H
#define ZEPHYR_INCLUDE_DRIVERS_STEPPER_H

/**
 * @brief Stepper Motor Controller Interface
 * @defgroup stepper_interface Stepper Motor Controller Interface
 * @since 4.0
 * @version 0.1.0
 * @ingroup io_interfaces
 * @{
 */

#include <errno.h>

#include <zephyr/types.h>
#include <zephyr/device.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * @brief Stepper motor directions.
 *
 * @details Stepper motors are manufactured with two coils of wire, resulting
 * in one winding per phase. By alternating the power between coils, as well
 * as the direction of the current, the motor is rotated. The stepper motor
 * can reverse the direction of rotation simply by reversing this sequence.
 * The wiring of the two phases, or more precisely the start and end of the
 * two coils, to the stepper motor driver determines the default direction
 * of rotation. Mostly this is "forward" or "right" direction for "positive"
 * and "backward" or "left" direction for "negative".
 *
 * @note When a stepper motor becomes engaged in software, and current is
 * applied to the coils, it may abruptly "snap" to the position that the
 * rotor is being held at.
 */
enum stepper_direction {
	STEPPER_DIRECTION_POSITIVE, /**< physical default direction */
	STEPPER_DIRECTION_NEGATIVE, /**< physical opposite direction */
};

/**
 * @brief Stepper motor microstep resolutions.
 *
 * @details Stepper motors move in discrete steps, or fractions of a
 * revolution. For example, a stepper motor with a 1.8° step angle will
 * make 200 steps for every full revolution of the motor (360° / 1.8°).
 * This discrete motion means the motor´s rotation isn´t perfectly smooth,
 * and the slower the rotation, the less smooth it is due to the relatively
 * large step size. One way to alleviate this lack of smoothness at slow
 * speeds is to reduce the size of the motor’s steps by microstepping.
 * Microstepping control divides each full step into smaller steps to help
 * smooth out the motor´s rotation. For example, a 1.8° step can be divided
 * up to 256 times, providing a step angle of 0.007° (1.8° / 256), or
 * 51,200 microsteps per revolution.
 *
 * @note: Not all stepper motor drivers allow microstepping. It is achieved
 * by using Pulse-Width Modulated (PWM) voltage to control current to the
 * motor windings. The driver sends two voltage sine waves, 90° out of phase,
 * to the motor windings. While current increases in one winding, it decreases
 * in the other winding. This gradual transfer of current results in smoother
 * motion and more consistent torque production than full- or half-step control.
 */
enum micro_step_resolution {
	STEPPER_MICRO_STEP_1,   /**< step angle x 1.   (full-step) */
	STEPPER_MICRO_STEP_2,   /**< step angle x 1/2. (half-step) */
	STEPPER_MICRO_STEP_4,   /**< step angle x 1/4. */
	STEPPER_MICRO_STEP_8,   /**< step angle x 1/8. */
	STEPPER_MICRO_STEP_16,  /**< step angle x 1/16. */
	STEPPER_MICRO_STEP_32,  /**< step angle x 1/32. */
	STEPPER_MICRO_STEP_64,  /**< step angle x 1/64. */
	STEPPER_MICRO_STEP_128, /**< step angle x 1/128. */
	STEPPER_MICRO_STEP_256, /**< step angle x 1/256. */
};

/**
 * @cond INTERNAL_HIDDEN
 *
 * For internal driver use only, skip these in public documentation.
 */

/**
 * @typedef stepper_api_enable
 * @brief API for enable or disable the stepper motor
 *
 * @see stepper_enable() for argument descriptions.
 */
typedef int (*stepper_api_enable)(const struct device *dev, const bool enable);

/**
 * @typedef stepper_api_move
 * @brief API for relative movement
 *
 * @see stepper_move() for argument descriptions.
 */
typedef int (*stepper_api_move)(const struct device *dev,
				const int32_t micro_steps);

/**
 * @typedef stepper_api_set_max_velocity
 * @brief API for setting maximum velocity
 *
 * @see stepper_set_max_velocity() for argument descriptions.
 */
typedef int (*stepper_api_set_max_velocity)(
			const struct device *dev,
			const uint32_t micro_steps_per_second);

/**
 * @typedef stepper_api_set_micro_step_res
 * @brief API for setting microstep resolution
 *
 * @see stepper_set_micro_step_res() for argument descriptions.
 */
typedef int (*stepper_api_set_micro_step_res)(
			const struct device *dev,
			const enum micro_step_resolution resolution);

/**
 * @typedef stepper_api_get_micro_step_res
 * @brief API for getting microstep resolution
 *
 * @see stepper_get_micro_step_res() for argument descriptions.
 */
typedef int (*stepper_api_get_micro_step_res)(
			const struct device *dev,
			enum micro_step_resolution *resolution);
/**
 * @typedef stepper_api_set_actual_position
 * @brief API for setting absolute position
 *
 * @see stepper_set_actual_position() for argument descriptions.
 */
typedef int (*stepper_api_set_actual_position)(const struct device *dev,
					       const int32_t position);

/**
 * @typedef stepper_api_get_actual_position
 * @brief API for getting absolute position
 *
 * @see stepper_get_actual_position() for argument descriptions.
 */
typedef int (*stepper_api_get_actual_position)(const struct device *dev,
					       int32_t *position);

/**
 * @typedef stepper_api_set_target_position
 * @brief API for setting absolute target position
 *
 * @see stepper_set_target_position() for argument descriptions.
 */
typedef int (*stepper_api_set_target_position)(const struct device *dev,
					       const int32_t position);

/**
 * @typedef stepper_api_is_moving
 * @brief API for getting stepper motor moving status.
 *
 * @see stepper_is_moving() for argument descriptions.
 */
typedef int (*stepper_api_is_moving)(const struct device *dev, bool *moving);

/**
 * @typedef stepper_api_enable_constant_velocity_mode
 * @brief API for enable constant velocity mode
 *
 * @see stepper_enable_constant_velocity_mode() for argument descriptions.
 */
typedef int (*stepper_api_enable_constant_velocity_mode)(
			const struct device *dev,
			const enum stepper_direction direction,
			const uint32_t velocity);

/**
 * @brief Stepper Motor Controller API
 */
__subsystem struct stepper_api {
	/* Mandatory callbacks. */
	stepper_api_enable enable;
	stepper_api_move move;
	stepper_api_set_max_velocity set_max_velocity;
	/* Optional callbacks. */
	stepper_api_set_micro_step_res set_micro_step_res;
	stepper_api_get_micro_step_res get_micro_step_res;
	stepper_api_set_actual_position set_actual_position;
	stepper_api_get_actual_position get_actual_position;
	stepper_api_set_target_position set_target_position;
	stepper_api_is_moving is_moving;
	stepper_api_enable_constant_velocity_mode enable_constant_velocity_mode;
};

/** @endcond */

/**
 * @brief API for enable or disable the stepper motor
 *
 * @details This routine turns either on or off the driven electric current
 * of the stepper motor.
 *
 * @param dev Stepper motor controller device instance
 * @param enable The status to set:
 *               false: disabled, electric current off
 *                true: enabled, electric current on
 *
 * @return 0 if successful
 * @return -EINVAL if enable is invalid or exceeds hardware capabilities
 * @return -ENOTSUP if API is not supported by hardware
 * @return -errno code if failure
 */
__syscall int stepper_enable(const struct device *dev, const bool enable);

static inline int z_impl_stepper_enable(const struct device *dev,
					const bool enable)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	return api->enable(dev, enable);
}

/**
 * @brief API for relative movement
 *
 * @details Set the microsteps to be moved from the current absolut position,
 * a.k.a. relative position movement.
 *
 * @param dev Stepper motor controller device instance
 * @param micro_steps The microsteps to set for relative movement
 *
 * @return 0 if successful
 * @return -EINVAL if micro_steps is invalid or exceeds hardware capabilities
 * @return -errno code if failure
 */
__syscall int stepper_move(const struct device *dev, const int32_t micro_steps);

static inline int z_impl_stepper_move(const struct device *dev,
				      const int32_t micro_steps)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	return api->move(dev, micro_steps);
}

/**
 * @brief API for setting maximum velocity
 *
 * @details Set the velocity to be reached by the stepper motor in microsteps
 * per seconds. For drivers such as DRV8825 where you toggle the STEP pin, the
 * pulse length would have to be calculated based on this parameter in the
 * driver. For drivers where velocity can be set, this parameter corresponds
 * to the maximum allowed velocity.
 *
 * @note Setting maximum velocity does not set the stepper motor into motion.
 * A combination of stepper_set_max_velocity() and stepper_move() is required
 * to set the stepper motor into motion.
 *
 * @param dev Stepper motor controller device instance
 * @param micro_steps_per_second The maximum velocity to set
 *
 * @return 0 if successful
 * @return -EINVAL if maximum velocity is invalid or exceeds hardware capabilities
 * @return -ENOTSUP if API is not supported by hardware
 * @return -errno code if failure
 */
__syscall int stepper_set_max_velocity(const struct device *dev,
				       const uint32_t micro_steps_per_second);

static inline int z_impl_stepper_set_max_velocity(
			const struct device *dev,
			uint32_t micro_steps_per_second)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	return api->set_max_velocity(dev, micro_steps_per_second);
}

/**
 * @brief API for setting microstep resolution
 *
 * @details Set the microstep resolution of the stepper motor.
 *
 * @param dev Stepper motor controller device instance
 * @param resolution The microstep resolution to set
 *
 * @return 0 if successful
 * @return -EINVAL if resolution is invalid or exceeds hardware capabilities
 * @return -ENOTSUP if API is not supported by hardware
 * @retval -ENOSYS if API not implemented by device driver
 * @return -errno code if failure
 */
__syscall int stepper_set_micro_step_res(
			const struct device *dev,
			const enum micro_step_resolution resolution);

static inline int z_impl_stepper_set_micro_step_res(
			const struct device *dev,
			const enum micro_step_resolution resolution)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	if (api->set_micro_step_res == NULL) {
		return -ENOSYS;
	}
	return api->set_micro_step_res(dev, resolution);
}

/**
 * @brief API for getting microstep resolution
 *
 * @details Get the microstep resolution of the stepper motor, that is
 * currently set.
 *
 * @param dev Stepper motor controller device instance
 * @param resolution Destination for the microstep resolution
 *
 * @return 0 if successful
 * @return -ENODATA if position has not been set
 * @return -ENOTSUP if API is not supported by hardware
 * @retval -ENOSYS if API not implemented by device driver
 * @return -errno code if failure
 */
__syscall int stepper_get_micro_step_res(
			const struct device *dev,
			enum micro_step_resolution *resolution);

static inline int z_impl_stepper_get_micro_step_res(
			const struct device *dev,
			enum micro_step_resolution *resolution)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	if (api->get_micro_step_res == NULL) {
		return -ENOSYS;
	}
	return api->get_micro_step_res(dev, resolution);
}

/**
 * @brief API for setting absolute position
 *
 * @details Set the actual absolut counted position of the stepper motor,
 * a.k.a. the reference position, in microsteps.
 *
 * @param dev Stepper motor controller device instance
 * @param position The actual position to set
 *
 * @return 0 if successful
 * @return -EINVAL if position is invalid or exceeds hardware capabilities
 * @return -ENOTSUP if API is not supported by hardware
 * @retval -ENOSYS if API not implemented by device driver
 * @return -errno code if failure
 */
__syscall int stepper_set_actual_position(const struct device *dev,
					  const int32_t position);

static inline int z_impl_stepper_set_actual_position(
			const struct device *dev, const int32_t position)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	if (api->set_actual_position == NULL) {
		return -ENOSYS;
	}
	return api->set_actual_position(dev, position);
}

/**
 * @brief API for getting absolute position
 *
 * @details Get the actual absolut counted position of the stepper motor,
 * a.k.a. the reference position, in microsteps.
 *
 * @param dev Stepper motor controller device instance
 * @param position Destination for the actual counted position
 *
 * @return 0 if successful
 * @return -ENODATA if position has not been set
 * @return -ENOTSUP if API is not supported by hardware
 * @retval -ENOSYS if API not implemented by device driver
 * @return -errno code if failure
 */
__syscall int stepper_get_actual_position(const struct device *dev,
					  int32_t *position);

static inline int z_impl_stepper_get_actual_position(
			const struct device *dev, int32_t *position)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	if (api->get_actual_position == NULL) {
		return -ENOSYS;
	}
	return api->get_actual_position(dev, position);
}

/**
 * @brief API for setting absolute target position
 *
 * @details Set the absolute target position of the stepper motor
 * in microsteps.
 *
 * @param dev Stepper motor controller device instance
 * @param position The absolut target position to set
 *
 * @return 0 if successful
 * @return -EINVAL if position is invalid or exceeds hardware capabilities
 * @return -ENOTSUP if API is not supported by hardware
 * @retval -ENOSYS if API not implemented by device driver
 * @return -errno code if failure
 */
__syscall int stepper_set_target_position(const struct device *dev,
					  const int32_t position);

static inline int z_impl_stepper_set_target_position(
			const struct device *dev, const int32_t position)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	if (api->set_target_position == NULL) {
		return -ENOSYS;
	}
	return api->set_target_position(dev, position);
}

/**
 * @brief API for getting stepper motor moving status.
 *
 * @details Check if the stepper motor is currently moving end get back
 * this moving status as an boolean.
 *
 * @param dev Stepper motor controller device instance
 * @param moving Destination for the moving status of the stepper motor
 *
 * @return 0 if successful
 * @return -ENODATA if moving has not been set
 * @return -ENOTSUP if API is not supported by hardware
 * @retval -ENOSYS if API not implemented by device driver
 * @return -errno code if failure
 */
__syscall int stepper_is_moving(const struct device *dev, bool *moving);

static inline int z_impl_stepper_is_moving(const struct device *dev,
					   bool *moving)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	if (api->is_moving == NULL) {
		return -ENOSYS;
	}
	return api->is_moving(dev, moving);
}

/**
 * @brief API for enable constant velocity mode
 *
 * @details Activate constant velocity mode with the given velocity in
 * micro_steps_per_second. If velocity > 0, motor shall be set into motion
 * and run incessantly until and unless stalled or stopped using some other
 * command, for instance, stepper_enable(..., false).
 *
 * @param dev Stepper motor controller device instance
 * @param direction The direction to set.
 * @param velocity The velocity to set:
 *                 > 0: Enable constant velocity mode with the given velocity
 *                      in a given direction.
 *                   0: Disable constant velocity mode.
 *
 * @return 0 if successful
 * @return -EINVAL if direction is invalid or exceeds hardware capabilities
 * @return -EINVAL if velocity is invalid or exceeds hardware capabilities
 * @return -ENOTSUP if API is not supported by hardware
 * @retval -ENOSYS if API not implemented by device driver
 * @return -errno code if failure
 */
__syscall int stepper_enable_constant_velocity_mode(
			const struct device *dev,
			const enum stepper_direction direction,
			const uint32_t velocity);

static inline int z_impl_stepper_enable_constant_velocity_mode(
			const struct device *dev,
			const enum stepper_direction direction,
			const uint32_t velocity)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;

	if (api->enable_constant_velocity_mode == NULL) {
		return -ENOSYS;
	}
	return api->enable_constant_velocity_mode(dev, direction, velocity);
}

/**
 * @}
 */

#ifdef __cplusplus
}
#endif

#include <syscalls/stepper.h>

#endif /* ZEPHYR_INCLUDE_DRIVERS_STEPPER_H */
