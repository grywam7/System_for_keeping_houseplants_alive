# System_for_keeping_houseplants_alive
Application designed for class: Programing in Python langugae 2025.
System is designed to work on esp32-wroom using MicroPython.

Main goal of the application is to keep potted plants in healthy condition.
It is an embedded system designed for the ESP32-WROOM
microcontroller with external sensors and connected LED lights. Main
functionalities are:
- determinig whether the plants need to be artificially irradiated, based
on weather data from an external API and scheduling irradiation for
a specified time,
- calculation of the amount of water needed to properly irrigate the
plant, based on previous soil moisture sensor measurements,
- exposing a web application for plant model management (CRUD
operations) and display of dynamically generated statistics for each
plant, such as a moisture chart. 


## Important Notice
As this requires a bit of RAM to run, my advice is to create your own micropython compilation for the ESP-32, without the Bluetooth module. You gain an extra 80KB of free memory, added to the initial 78KB, doubling it, so you don't have to care about the AOM error anymore.
