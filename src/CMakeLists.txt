if (TARGET tinyusb_device)
    add_executable(timer
            timer.c
            )

    # pull in common dependencies
    target_link_libraries(timer pico_stdlib hardware_gpio)

    # enable usb output, disable uart output
    pico_enable_stdio_usb(timer 1)
    pico_enable_stdio_uart(timer 1)

    # create map/bin/hex/uf2 file etc.
    pico_add_extra_outputs(timer)

    # add url via pico_set_program_url
    example_auto_set_url(timer)
elseif(PICO_ON_DEVICE)
    message(WARNING "not building timer because TinyUSB submodule is not initialized in the SDK")
endif()
