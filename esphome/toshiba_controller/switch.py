import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch

from . import ToshibaController, toshiba_controller_ns

CONF_TOSHIBA_CONTROLLER_ID = "toshiba_controller_id"

CustomSwitch = toshiba_controller_ns.class_("CustomSwitch", switch.Switch)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_TOSHIBA_CONTROLLER_ID): cv.use_id(ToshibaController),
        cv.Optional("internal_thermistor"): switch.switch_schema(
            CustomSwitch,
            icon="mdi:thermometer",
        ),
        cv.Optional("ionizer"): switch.switch_schema(
            CustomSwitch,
            icon="mdi:pine-tree",
        ),
    }
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_TOSHIBA_CONTROLLER_ID])

    if therm_config := config.get("internal_thermistor"):
        sw = cg.new_Pvariable(therm_config[cv.CONF_ID])
        await switch.register_switch(sw, therm_config)
        cg.add(hub.set_internal_thermistor_switch_obj(sw))

    if ionizer_config := config.get("ionizer"):
        sw = cg.new_Pvariable(ionizer_config[cv.CONF_ID])
        await switch.register_switch(sw, ionizer_config)
        cg.add(hub.set_ionizer_switch_obj(sw))
