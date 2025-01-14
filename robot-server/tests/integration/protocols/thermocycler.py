metadata = {
    "protocolName": "Thermocycler test",
    "author": "Opentrons <protocols@opentrons.com>",
    "apiLevel": "2.4",
}


def run(ctx):
    thermocycler = ctx.load_module("thermocycler module", "7")
    thermocycler.load_labware("nest_96_wellplate_2ml_deep", "deepwell plate")
