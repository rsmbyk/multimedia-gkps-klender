import * as settings from '../../../common/settings.js'
import * as settingsStorage from '../../../common/settings-storage.js'

import * as options from '../common/options.js'

import * as pasteModal from '../modals/paste.js'

const settingsButton = $('#display-button-settings')

const updateNumberOfLinesSelection = numberOfLines => {
    settingsButton.find(`.item[data-settings='numberOfLines'] > .icon`).hide()
    settingsButton.find(`.item[data-value='settings-numberOfLines-${numberOfLines}'] > .icon`).show()
}

settingsButton
    .dropdown()
    .dropdown('setting', 'onChange', value => {
        if (value === 'paste') {
            pasteModal.open()
        }
        else if (value === 'settings-settings') {
            settings.open()
        }
        else if (value.startsWith('settings')) {
            const [_, settingName, settingValue] = value.split('-')

            switch (settingName) {
                case 'numberOfLines':
                    options.setNumberOfLines(parseInt(settingValue))
                    break
                default:
                    break
            }
        }
    })

settingsStorage.setPrefix('OBS_SONGS')
options.numberOfLinesSubject.subscribe(updateNumberOfLinesSelection)
