import * as settings from '../../../../common/settings.js'
import * as settingsStorage from '../../../../common/settings-storage.js'

import * as pasteModal from '../../modals/paste.js'

const settingsButton = $('#display-button-settings')

settingsButton
    .dropdown()
    .dropdown('setting', 'onChange', value => {
        if (value === 'paste') {
            pasteModal.open()
        }
        else if (value === 'settings-settings') {
            settings.open()
        }
    })

settingsStorage.setPrefix('OBS_TATIB')
