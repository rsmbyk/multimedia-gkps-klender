import * as pasteModal from '../modals/paste.js'

const settingsButton = $('#display-button-settings')

settingsButton
    .dropdown()
    .dropdown('setting', 'onChange', value => {
        if (value === 'paste') {
            pasteModal.open()
        }
    })
