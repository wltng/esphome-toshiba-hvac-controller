import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, select, sensor, uart
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
)

CODEOWNERS = []
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["climate", "sensor", "switch", "select"]

toshiba_controller_ns = cg.esphome_ns
ToshibaController = toshiba_controller_ns.class_(
    "ToshibaController", climate.Climate, cg.Component
)

CONF_TEMPERATURE_SENSOR_ID = "temperature_sensor_id"
CONF_SPECIAL_MODE_SELECT_ID = "special_mode_select_id"
CONF_SILENT_MODE_SELECT_ID = "silent_mode_select_id"
CONF_FIREPLACE_SELECT_ID = "fireplace_select_id"
CONF_SWING_MODE_SELECT_ID = "swing_mode_select_id"
CONF_FIXED_POSITION_SELECT_ID = "fixed_position_select_id"
CONF_POWER_SELECT_ID = "power_select_id"
CONF_SMART_THERMOSTAT_MULTIPLIER = "smart_thermostat_multiplier"
CONF_SMART_THERMOSTAT_RUNAWAY_PROTECTION = "smart_thermostat_runaway_protection"
CONF_DISABLE_COOLING_MODES = "disable_cooling_modes"

# Sensor output configs
CONF_OUTDOOR_TEMPERATURE = "outdoor_temperature"
CONF_FCU_AIR_TEMP = "fcu_air_temp"
CONF_FCU_SETPOINT = "fcu_setpoint"
CONF_FCU_TC_TEMP = "fcu_tc_temp"
CONF_FCU_TCJ_TEMP = "fcu_tcj_temp"
CONF_FCU_FAN_RPM = "fcu_fan_rpm"
CONF_CDU_TD_TEMP = "cdu_td_temp"
CONF_CDU_TS_TEMP = "cdu_ts_temp"
CONF_CDU_TE_TEMP = "cdu_te_temp"
CONF_CDU_LOAD = "cdu_load"
CONF_CDU_IAC = "cdu_iac"

CONFIG_SCHEMA = (
    climate.climate_schema(ToshibaController)
    .extend(
        {
            cv.Required("uart_id"): cv.use_id(uart.UARTComponent),
            cv.Required(CONF_TEMPERATURE_SENSOR_ID): cv.use_id(sensor.Sensor),
            cv.Required(CONF_SPECIAL_MODE_SELECT_ID): cv.use_id(select.Select),
            cv.Optional(CONF_SILENT_MODE_SELECT_ID): cv.use_id(select.Select),
            cv.Optional(CONF_FIREPLACE_SELECT_ID): cv.use_id(select.Select),
            cv.Required(CONF_SWING_MODE_SELECT_ID): cv.use_id(select.Select),
            cv.Optional(CONF_FIXED_POSITION_SELECT_ID): cv.use_id(select.Select),
            cv.Required(CONF_POWER_SELECT_ID): cv.use_id(select.Select),
            cv.Optional(CONF_SMART_THERMOSTAT_MULTIPLIER, default=3.0): cv.float_range(
                min=1.0, max=10.0
            ),
            cv.Optional(
                CONF_SMART_THERMOSTAT_RUNAWAY_PROTECTION, default=True
            ): cv.boolean,
            cv.Optional(CONF_DISABLE_COOLING_MODES, default=False): cv.boolean,
            # Sensor outputs
            cv.Optional(CONF_OUTDOOR_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:home-thermometer-outline",
            ),
            cv.Optional(CONF_FCU_AIR_TEMP): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:thermometer",
            ),
            cv.Optional(CONF_FCU_SETPOINT): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:thermometer",
            ),
            cv.Optional(CONF_FCU_TC_TEMP): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:thermometer",
            ),
            cv.Optional(CONF_FCU_TCJ_TEMP): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:thermometer",
            ),
            cv.Optional(CONF_FCU_FAN_RPM): sensor.sensor_schema(
                unit_of_measurement="rpm",
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:fan",
            ),
            cv.Optional(CONF_CDU_TD_TEMP): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:thermometer",
            ),
            cv.Optional(CONF_CDU_TS_TEMP): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:thermometer",
            ),
            cv.Optional(CONF_CDU_TE_TEMP): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:thermometer",
            ),
            cv.Optional(CONF_CDU_LOAD): sensor.sensor_schema(
                unit_of_measurement="%",
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:heat-pump-outline",
            ),
            cv.Optional(CONF_CDU_IAC): sensor.sensor_schema(
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)

    uart_comp = await cg.get_variable(config["uart_id"])
    cg.add(var.set_uart(uart_comp))

    temp_sensor = await cg.get_variable(config[CONF_TEMPERATURE_SENSOR_ID])
    cg.add(var.set_temperature_sensor(temp_sensor))

    special = await cg.get_variable(config[CONF_SPECIAL_MODE_SELECT_ID])
    cg.add(var.set_special_mode_select(special))

    swing = await cg.get_variable(config[CONF_SWING_MODE_SELECT_ID])
    cg.add(var.set_swing_mode_select(swing))

    power = await cg.get_variable(config[CONF_POWER_SELECT_ID])
    cg.add(var.set_power_select(power))

    cg.add(var.set_smart_thermostat_multiplier(config[CONF_SMART_THERMOSTAT_MULTIPLIER]))
    cg.add(var.set_smart_thermostat_runaway_protection(config[CONF_SMART_THERMOSTAT_RUNAWAY_PROTECTION]))
    cg.add(var.set_disable_cooling_modes(config[CONF_DISABLE_COOLING_MODES]))

    # Wire up optional extra selects
    if CONF_SILENT_MODE_SELECT_ID in config:
        silent_sel = await cg.get_variable(config[CONF_SILENT_MODE_SELECT_ID])
        cg.add(var.set_silent_mode_select_ptr(silent_sel))
    if CONF_FIREPLACE_SELECT_ID in config:
        fireplace_sel = await cg.get_variable(config[CONF_FIREPLACE_SELECT_ID])
        cg.add(var.set_fireplace_select_ptr(fireplace_sel))
    if CONF_FIXED_POSITION_SELECT_ID in config:
        fixed_pos_sel = await cg.get_variable(config[CONF_FIXED_POSITION_SELECT_ID])
        cg.add(var.set_fixed_position_select_ptr(fixed_pos_sel))

    # Wire up optional sensor outputs
    sensor_map = [
        (CONF_OUTDOOR_TEMPERATURE, "set_outdoor_temperature_sensor"),
        (CONF_FCU_AIR_TEMP,        "set_fcu_air_temp_sensor"),
        (CONF_FCU_SETPOINT,        "set_fcu_setpoint_sensor"),
        (CONF_FCU_TC_TEMP,         "set_fcu_tc_temp_sensor"),
        (CONF_FCU_TCJ_TEMP,        "set_fcu_tcj_temp_sensor"),
        (CONF_FCU_FAN_RPM,         "set_fcu_fan_rpm_sensor"),
        (CONF_CDU_TD_TEMP,         "set_cdu_td_temp_sensor"),
        (CONF_CDU_TS_TEMP,         "set_cdu_ts_temp_sensor"),
        (CONF_CDU_TE_TEMP,         "set_cdu_te_temp_sensor"),
        (CONF_CDU_LOAD,            "set_cdu_load_sensor"),
        (CONF_CDU_IAC,             "set_cdu_iac_sensor"),
    ]
    for conf_key, setter in sensor_map:
        if conf_key in config:
            sens = await sensor.new_sensor(config[conf_key])
            cg.add(getattr(var, setter)(sens))
