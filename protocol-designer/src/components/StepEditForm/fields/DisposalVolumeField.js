// @flow
import * as React from 'react'
import {
  FormGroup,
  CheckboxField,
  DropdownField,
  type Options,
} from '@opentrons/components'
import { connect } from 'react-redux'
import cx from 'classnames'

import { i18n } from '../../../localization'
import { getMaxDisposalVolumeForMultidispense } from '../../../steplist/formLevel/handleFormChange/utils'
import { selectors as stepFormSelectors } from '../../../step-forms'
import { selectors as uiLabwareSelectors } from '../../../ui/labware'
import { getBlowoutLocationOptionsForForm } from '../utils'
import { TextField } from './TextField'

import type { FieldProps, FieldPropsByName } from '../types'
import type { BaseState } from '../../../types'

import styles from '../StepEditForm.css'

type DropdownFormFieldProps = {|
  ...FieldProps,
  className?: string,
  options: Options,
|}
const DropdownFormField = (props: DropdownFormFieldProps) => {
  return (
    <DropdownField
      options={props.options}
      value={props.value ? String(props.value) : null}
      onBlur={props.onFieldBlur}
      onChange={props.updateValue}
      onFocus={props.onFieldFocus}
    />
  )
}

type SP = {|
  disposalDestinationOptions: Options,
  maxDisposalVolume: ?number,
|}
type OP = {| propsForFields: FieldPropsByName |}
type Props = { ...SP, ...OP }

const DisposalVolumeFieldComponent = (props: Props) => {
  const { propsForFields } = props

  const { maxDisposalVolume } = props
  const volumeBoundsCaption =
    maxDisposalVolume != null
      ? `max ${maxDisposalVolume} ${i18n.t('application.units.microliter')}`
      : null

  const volumeField = (
    <div>
      <TextField
        {...propsForFields['disposalVolume_volume']}
        caption={volumeBoundsCaption}
        className={cx(styles.small_field, styles.orphan_field)}
        units={i18n.t('application.units.microliter')}
      />
    </div>
  )

  const { value, updateValue } = propsForFields['disposalVolume_checkbox']

  return (
    <FormGroup label={i18n.t('form.step_edit_form.multiDispenseOptionsLabel')}>
      <React.Fragment>
        <div
          className={cx(styles.checkbox_row, {
            [styles.captioned_field]: volumeBoundsCaption,
          })}
        >
          <CheckboxField
            label="Disposal Volume"
            value={Boolean(value)}
            className={cx(styles.checkbox_field, styles.large_field)}
            onChange={(e: SyntheticInputEvent<*>) => updateValue(!value)}
          />
          {value ? volumeField : null}
        </div>
        {value ? (
          <div className={styles.checkbox_row}>
            <div className={styles.sub_label_no_checkbox}>Blowout</div>
            <DropdownFormField
              {...propsForFields['blowout_location']}
              className={styles.large_field}
              options={props.disposalDestinationOptions}
            />
          </div>
        ) : null}
      </React.Fragment>
    </FormGroup>
  )
}
const mapSTP = (state: BaseState): SP => {
  const rawForm = stepFormSelectors.getUnsavedForm(state)
  return {
    maxDisposalVolume: getMaxDisposalVolumeForMultidispense(
      rawForm,
      stepFormSelectors.getPipetteEntities(state)
    ),
    disposalDestinationOptions: getBlowoutLocationOptionsForForm(
      uiLabwareSelectors.getDisposalLabwareOptions(state),
      rawForm
    ),
  }
}

export const DisposalVolumeField: React.AbstractComponent<OP> = connect<
  Props,
  OP,
  SP,
  _,
  _,
  _
>(mapSTP)(DisposalVolumeFieldComponent)
