.. _colorful-sample:

Colorful
########

Draw an RGB color gradient on a display device.

Overview
********

This sample uses the :external+zephyr:ref:`display API <display_api>`
to draw an RGB color gradient onto the display.

For most display controllers, the RGB color gradient runs across the entire screen
from red to green, then from green to blue, and finally from blue back to red. The
cycle repeats endlessly.

.. raw:: html

   <style>
     .zephyr-display-sample {
       position: relative;
       width: 320px;
       height: 240px;
       margin: auto;
       background: white;
       border: 1px solid #ccc;
       box-sizing: border-box;
     }

     .zephyr-display-sample .entire {
       position: absolute;
       width: 318px;
       height: 238px;
     }

     /* RGB variant */
     .zephyr-display-sample--rgb .cg {
       top: 0;
       left: 0;
       background: white;
       animation: zephyr-display-rgb-toggle 9s linear infinite;
     }

     /* Mono variant */
     .zephyr-display-sample--mono .cg {
       top: 0;
       left: 0;
       background: white;
       animation: zephyr-display-gray-toggle 9s linear infinite;
     }

     /* 1bpp variant */
     .zephyr-display-sample--1bpp .cg {
       top: 0;
       left: 0;
       background: white;
       animation: zephyr-display-bw-toggle 0.6s steps(2, jump-none) infinite;
     }

     @keyframes zephyr-display-bw-toggle {
       from { background-color: black; }
       to   { background-color: white; }
     }

     /* Quick RGB to luminance: Y = (2 * r + 5 * g + 1 * b) >> 3 */
     @keyframes zephyr-display-gray-toggle {
       0%, 100% {
         /* rgb:#FF0000 -> Y:#3F3F3F */
         background-color: rgb(63, 63, 63);
       }
       16% {
         /* rgb:#7F7F00 -> Y:#6F6F6F */
         background-color: rgb(111, 111, 111);
       }
       32% {
         /* rgb:#00FF00 -> Y:#9F9F9F */
         background-color: rgb(159, 159, 159);
       }
       50% {
         /* rgb:#007F7F -> Y:#5F5F5F */
         background-color: rgb(95, 95, 95);
       }
       66% {
         /* rgb:#0000FF -> Y:#1F1F1F */
         background-color: rgb(31, 31, 31);
       }
       82% {
         /* rgb:#7F007F -> Y:#2F2F2F */
         background-color: rgb(47, 47, 47);
       }
     }

     @keyframes zephyr-display-rgb-toggle {
       0%, 100% {
         /* rgb:#FF0000 */
         background-color: rgb(255, 0, 0);
       }
       16% {
         /* rgb:#7F7F00 */
         background-color: rgb(127, 127, 0);;
       }
       32% {
         /* rgb:#00FF00 */
         background-color: rgb(0, 255, 0);;
       }
       50% {
         /* rgb:#007F7F */
         background-color: rgb(0, 127, 127);;
       }
       66% {
         /* rgb:#0000FF */
         background-color: rgb(0, 0, 255);;
       }
       82% {
         /* rgb:#7F007F */
         background-color: rgb(127, 0, 127);;
       }
     }
   </style>

.. tabs::

   .. tab:: RGB

      .. raw:: html

         <figure class="zephyr-display-sample-wrap">
           <div class="zephyr-display-sample zephyr-display-sample--rgb" aria-hidden="true">
             <div class="entire cg"></div>
           </div>
           <figcaption>
             <p>
               <span class="caption-text">
                Typical RGB output at 320x240: color gradient from red across dark yellow to green,
                across dark cyan to blue, across dark magenta back to red.
               </span>
             </p>
           </figcaption>
         </figure>

   .. tab:: Grayscale

      On displays using a multi-bit luminance format (for example :c:enumerator:`PIXEL_FORMAT_L_8`),
      the entire screen runs over different grey level between black and white (color luminance).
      Other multi-bit monochrome formats behave similarly (different greys).

      .. raw:: html

         <figure class="zephyr-display-sample-wrap">
           <div class="zephyr-display-sample zephyr-display-sample--mono" aria-hidden="true">
             <div class="entire cg"></div>
           </div>
           <figcaption>
             <p>
               <span class="caption-text">
                Grayscale-style; entire screen animates through different greys (color luminance).
               </span>
             </p>
           </figcaption>
         </figure>

   .. tab:: 1 bpp

      On displays with 1 bit per pixel, the greyscale animation of the entire screen will appear as
      flickering between black and white.

      .. raw:: html

         <figure class="zephyr-display-sample-wrap">
           <div class="zephyr-display-sample zephyr-display-sample--1bpp" aria-hidden="true">
             <div class="entire cg"></div>
           </div>
          <figcaption>
             <p>
               <span class="caption-text">
               1 bpp: entire screen animates flickering between fore- and background color (black
               for <code>MONO01</code>, white for <code>MONO10</code> on a black screen).
               </span>
             </p>
          </figcaption>
         </figure>

   .. tab:: E-paper

      By querying the display controller's capabilities, it is possible to determine if the display
      is an e-paper display by checking if the :c:enumerator:`SCREEN_INFO_EPD` bit is set in the
      :c:member:`display_capabilities.screen_info`.

      For such displays, the color of the entire screen will change at a much slower rate than
      on a typical LCD, to align with the typical refresh rate of e-ink technologies.

Building and Running
********************

As this is a generic sample it should work with any display supported by Zephyr.

Below is an example on how to build for a :external+zephyr:zephyr:board:`nrf52840dk`
board with a :external+zephyr:ref:`adafruit_2_8_tft_touch_v2`.

.. zephyr-app-commands::
   :app: bridle/samples/colorful
   :build-dir: colorful
   :board: nrf52840dk/nrf52840
   :shield: adafruit_2_8_tft_touch_v2
   :goals: build
   :compact:

For testing purpose without the need of any hardware, the
:external+zephyr:zephyr:board:`native_sim/native/64 <native_sim>`
board is also supported and can be built as follows:

.. zephyr-app-commands::
   :app: bridle/samples/colorful
   :build-dir: colorful
   :board: native_sim/native/64
   :goals: run
   :compact:

Twister test suites
===================

To run the test with twister on emulated or dummy hardware,
use the following command:

.. code-block:: shell

   west twister -v -X fixture_display -T bridle/samples/colorful -s sample.colorful.sdl -s sample.colorful.dummy

To run all test with twister, use the following command:

.. code-block:: shell

   west twister -v -T bridle/samples/colorful

List of Arduino-based display shields
*************************************

- :external+zephyr:ref:`adafruit_2_8_tft_touch_v2`
- :external+zephyr:ref:`ssd1306_128_shield`
- :external+zephyr:ref:`st7789v_generic`
- :external+zephyr:ref:`waveshare_epaper`
