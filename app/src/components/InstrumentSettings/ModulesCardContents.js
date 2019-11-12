// @flow
import * as React from 'react'

import ModuleItem, { NoModulesMessage } from '../ModuleItem'

import type { Robot } from '../../discovery/types'
import type { Module } from '../../robot-api/types'

type Props = {
  robot: Robot,
  modules: Array<Module>,
}

export default function ModulesCardContents(props: Props) {
  const { modules, robot } = props
  if (modules.length === 0) return <NoModulesMessage />

  return (
    <React.Fragment>
      {modules.map((mod, index) => (
        <ModuleItem module={mod} key={index} robot={robot} />
      ))}
    </React.Fragment>
  )
}
