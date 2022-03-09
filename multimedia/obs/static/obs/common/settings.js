import * as mutations from '/static/helpers/mutations.js'

import * as settingsStorage from './settings-storage.js'

const modal = $('#modal-settings')

const form = $('#modal-settings-form')

const dropdownTitleTextSize = $('#modal-settings-form-title-size-dropdown')

const dropdownContentTextSize = $('#modal-settings-form-content-size-dropdown')

const buttonBackgroundColourApply = $('#modal-settings-form-background-colour-button-apply')
const buttonBackgroundColourReset = $('#modal-settings-form-background-colour-button-reset')

const buttonLabelColourApply = $('#modal-settings-form-label-colour-button-apply')
const buttonLabelColourReset = $('#modal-settings-form-label-colour-button-reset')

const sliderOpacity = $('#modal-settings-form-opacity-slider')
const inputOpacity = $('#modal-settings-form-opacity-input')
const buttonOpacityReset = $('#modal-settings-form-opacity-button-reset')

mutations.observeFlexModal(modal[0])

form.form({
    fields: {
        backgroundColour: {
            rules: [
                {
                    type: 'empty',
                },
                {
                    type: 'regExp[/^([0-9a-f]{3}|[0-9a-f]{4}|[0-9a-f]{6}|[0-9a-f]{8})$/i]',
                    prompt: '{name} must be in hex colour format.',
                },
            ],
        },
        labelColour: {
            rules: [
                {
                    type: 'empty',
                },
                {
                    type: 'regExp[/^([0-9a-f]{3}|[0-9a-f]{4}|[0-9a-f]{6}|[0-9a-f]{8})$/i]',
                    prompt: '{name} must be in hex colour format.',
                },
            ],
        },
    },
    inline: true,
})

dropdownTitleTextSize.dropdown({
    showOnFocus: false,
})
dropdownTitleTextSize.dropdown('setting', 'onChange', value => {
    settingsStorage.setTitleTextSize(value)
})

dropdownContentTextSize.dropdown()
dropdownContentTextSize.dropdown('setting', 'onChange', value => {
    settingsStorage.setContentTextSize(value)
})

buttonBackgroundColourApply.click(() => {
    if (form.form('is valid', 'backgroundColour')) {
        settingsStorage.setBackgroundColour(form.form('get value', 'backgroundColour'))
    } else {
        form.form('validate field', 'backgroundColour')
    }
})

buttonLabelColourApply.click(() => {
    if (form.form('is valid', 'labelColour')) {
        settingsStorage.setLabelColour(form.form('get value', 'labelColour'))
    } else {
        form.form('validate field', 'labelColour')
    }
})

buttonBackgroundColourReset.click(() => {
    settingsStorage.resetBackgroundColour()
})

buttonLabelColourReset.click(() => {
    settingsStorage.resetLabelColour()
})

buttonOpacityReset.click(() => {
    settingsStorage.resetOpacity()
})

sliderOpacity.slider({
    min: 0,
    max: 1,
    step: 0,
}).slider('setting', 'onMove', value => {
    settingsStorage.setOpacity(value)
    form.form('set value', 'opacity', value)
})

const updateDropdownTitleTextSize = titleTextSize => {
    dropdownTitleTextSize.dropdown('set selected', titleTextSize)
}

const updateDropdownContentTextSize = contentTextSize => {
    dropdownContentTextSize.dropdown('set selected', contentTextSize)
}

const updateBackgroundColourValue = backgroundColour => {
    form.form('set value', 'backgroundColour', backgroundColour)
}

const updateLabelColourValue = labelColour => {
    form.form('set value', 'labelColour', labelColour)
}

const updateSliderOpacity = opacity => {
    sliderOpacity.slider('set value', opacity)
}

export const open = () => {
    modal.modal('show')
}

settingsStorage.titleTextSizeSubject.subscribe(updateDropdownTitleTextSize)
settingsStorage.contentTextSizeSubject.subscribe(updateDropdownContentTextSize)
settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColourValue)
settingsStorage.labelColourSubject.subscribe(updateLabelColourValue)
settingsStorage.opacitySubject.subscribe(updateSliderOpacity)
