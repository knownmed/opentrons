import type { AirGapParams } from '@opentrons/shared-data/lib/protocol/types/schemaV3';
import type { CommandCreator } from '../../types';
/** Dispense with given args. Requires tip. */
export declare const dispenseAirGap: CommandCreator<AirGapParams>;
