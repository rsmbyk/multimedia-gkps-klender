import * as settings from '../../../common/settings.js'
import * as settingsStorage from '../../../common/settings-storage.js'

const buttonSettings = $('#display-button-settings')

buttonSettings.click(() => settings.open())

settingsStorage.setPrefix('OBS_BIBLE')
