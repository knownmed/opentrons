// constants for dealing with robot coordinate system (eg in labwareTools)
export const SLOT_LENGTH_MM = 127.76 // along X axis in robot coordinate system

export const SLOT_WIDTH_MM = 85.48 // along Y axis in robot coordinate system

// constants for SVG renders of the deck
export const SLOT_RENDER_WIDTH = SLOT_LENGTH_MM // along X axis in SVG coords

export const SLOT_RENDER_HEIGHT = SLOT_WIDTH_MM // along Y axis in SVG coords

// taken from opentrons_1_trash_1100ml_fixed v1's dimensions
export const FIXED_TRASH_RENDER_HEIGHT = 165.86 // along Y axis in SVG coords

// used for module visualization, remove this when we start using actual module dimensions
export const STD_SLOT_X_DIM = 128
export const STD_SLOT_Y_DIM = 86
export const STD_SLOT_DIVIDER_WIDTH = 4

export const OPENTRONS_LABWARE_NAMESPACE = 'opentrons'
export const FIXED_TRASH_ID = 'trashId'

// TODO: IL 2020-02-19 These 3 constants are DEPRECATED because they're ambiguous model vs type.
export const THERMOCYCLER: 'thermocycler' = 'thermocycler'
export const TEMPDECK: 'tempdeck' = 'tempdeck'
export const MAGDECK: 'magdeck' = 'magdeck'

// these are the Module Def Schema v2 equivalents of the above. They should match the names of JSON definitions
// in shared-data/module/definitions/2.
export const MAGNETIC_MODULE_V1: 'magneticModuleV1' = 'magneticModuleV1'
export const MAGNETIC_MODULE_V2: 'magneticModuleV2' = 'magneticModuleV2'
export const TEMPERATURE_MODULE_V1: 'temperatureModuleV1' =
  'temperatureModuleV1'
export const TEMPERATURE_MODULE_V2: 'temperatureModuleV2' =
  'temperatureModuleV2'
export const THERMOCYCLER_MODULE_V1: 'thermocyclerModuleV1' =
  'thermocyclerModuleV1'

// pipette display categories
export const GEN2: 'GEN2' = 'GEN2'
export const GEN1: 'GEN1' = 'GEN1'

// pipette mounts
export const LEFT: 'left' = 'left'
export const RIGHT: 'right' = 'right'

// fake slot that PD uses to represent the slot the thermocycler sits in
export const SPAN7_8_10_11_SLOT: 'span7_8_10_11' = 'span7_8_10_11'

// NOTE: these are NOT module MODELs, they are `moduleType`s. Should match ENUM in module definition file.
export const TEMPERATURE_MODULE_TYPE: 'temperatureModuleType' =
  'temperatureModuleType'
export const MAGNETIC_MODULE_TYPE: 'magneticModuleType' = 'magneticModuleType'
export const THERMOCYCLER_MODULE_TYPE: 'thermocyclerModuleType' =
  'thermocyclerModuleType'

export const MAGNETIC_MODULE_MODELS = [MAGNETIC_MODULE_V1, MAGNETIC_MODULE_V2]

export const TEMPERATURE_MODULE_MODELS = [
  TEMPERATURE_MODULE_V1,
  TEMPERATURE_MODULE_V2,
]

export const THERMOCYCLER_MODULE_MODELS = [THERMOCYCLER_MODULE_V1]

export const MODULE_MODELS = [
  ...MAGNETIC_MODULE_MODELS,
  ...TEMPERATURE_MODULE_MODELS,
  ...THERMOCYCLER_MODULE_MODELS,
]

export const MODULE_TYPES = [
  TEMPERATURE_MODULE_TYPE,
  MAGNETIC_MODULE_TYPE,
  THERMOCYCLER_MODULE_TYPE,
]

export const GEN_ONE_MULTI_PIPETTES = ['p10_multi', 'p50_multi', 'p300_multi']
