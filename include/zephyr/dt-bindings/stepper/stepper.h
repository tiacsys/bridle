/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 Carl Zeiss Meditec AG
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_STEPPER_STEPPER_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_STEPPER_STEPPER_H_

/**
 * @brief Stepper Motor Interface
 * @defgroup stepper_interface Stepper Motor Interface
 * @ingroup io_interfaces
 * @{
 */

/**
 * @name Stepper motor microstep resolution flags.
 *
 * @details Stepper motors move in discrete steps, or fractions of a
 * revolution. For example, a stepper motor with a 1.8° step angle will
 * make 200 steps for every full revolution of the motor (360° / 1.8°).
 * This discrete motion means the motor´s rotation isn't perfectly smooth,
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
 *
 * @{
 */

#define STEPPER_USTEP_RES_1   (1U << 0) /**< step angle x 1. */
#define STEPPER_USTEP_RES_2   (1U << 1) /**< step angle x 1/2. */
#define STEPPER_USTEP_RES_4   (1U << 2) /**< step angle x 1/4. */
#define STEPPER_USTEP_RES_8   (1U << 3) /**< step angle x 1/8. */
#define STEPPER_USTEP_RES_16  (1U << 4) /**< step angle x 1/16. */
#define STEPPER_USTEP_RES_32  (1U << 5) /**< step angle x 1/32. */
#define STEPPER_USTEP_RES_64  (1U << 6) /**< step angle x 1/64. */
#define STEPPER_USTEP_RES_128 (1U << 7) /**< step angle x 1/128. */
#define STEPPER_USTEP_RES_256 (1U << 8) /**< step angle x 1/256. */

/** @} */

/**
 * @}
 */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_STEPPER_STEPPER_H_ */
