import * as React from 'react'
import { FileUploadMessageModal as FileUploadMessageModalComponent } from './FileUploadMessageModal'
import { connect } from 'react-redux'
import {
  selectors as loadFileSelectors,
  actions as loadFileActions,
} from '../../../load-file'
import { Dispatch } from 'redux'
import { BaseState } from '../../../types'
type Props = React.ComponentProps<typeof FileUploadMessageModalComponent>
interface SP {
  message: Props['message']
}
type DP = Omit<Props, keyof SP>

function mapStateToProps(state: BaseState): SP {
  return {
    message: loadFileSelectors.getFileUploadMessages(state),
  }
}

function mapDispatchToProps(dispatch: Dispatch<any>): DP {
  return {
    cancelProtocolMigration: () => dispatch(loadFileActions.undoLoadFile()),
    dismissModal: () => dispatch(loadFileActions.dismissFileUploadMessage()),
  }
}

export const FileUploadMessageModal = connect(
  mapStateToProps,
  mapDispatchToProps
)(FileUploadMessageModalComponent)