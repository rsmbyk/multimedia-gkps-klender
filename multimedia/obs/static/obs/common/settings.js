import * as mutations from '/static/helpers/mutations.js'

import * as settingsStorage from './settings-storage.js'

const modal = $('#modal-settings')

const form = $('#modal-settings-form')

const sliderTitleSize = $('#modal-settings-form-title-size-slider')
const inputTitleSize = $('#modal-settings-form-title-size-input')
const buttonTitleSizeApply = $('#modal-settings-form-title-size-button-apply')
const buttonTitleSizeReset = $('#modal-settings-form-title-size-button-reset')

const sliderContentSize = $('#modal-settings-form-content-size-slider')
const inputContentSize = $('#modal-settings-form-content-size-input')
const buttonContentSizeApply = $('#modal-settings-form-content-size-button-apply')
const buttonContentSizeReset = $('#modal-settings-form-content-size-button-reset')

const buttonTextColourApply = $('#modal-settings-form-text-colour-button-apply')
const buttonTextColourReset = $('#modal-settings-form-text-colour-button-reset')

const buttonBackgroundColourApply = $('#modal-settings-form-background-colour-button-apply')
const buttonBackgroundColourReset = $('#modal-settings-form-background-colour-button-reset')

const buttonLabelBackgroundColourApply = $('#modal-settings-form-label-background-colour-button-apply')
const buttonLabelBackgroundColourReset = $('#modal-settings-form-label-background-colour-button-reset')

const sliderOpacity = $('#modal-settings-form-opacity-slider')
const inputOpacity = $('#modal-settings-form-opacity-input')
const buttonOpacityReset = $('#modal-settings-form-opacity-button-reset')

mutations.observeFlexModal(modal[0])

form.form({
    fields: {
        titleSize: {
            rules: [
                {
                    type: 'empty',
                },
                {
                    type: `integer[${settingsStorage.textSizeMinValue}..${settingsStorage.textSizeMaxValue}]`,
                },
            ],
        },
        contentSize: {
            rules: [
                {
                    type: 'empty',
                },
                {
                    type: `integer[${settingsStorage.textSizeMinValue}..${settingsStorage.textSizeMaxValue}]`,
                },
            ],
        },
        textColour: {
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
        labelBackgroundColour: {
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

buttonTitleSizeApply.click(() => {
    if (form.form('is valid', 'titleSize')) {
        settingsStorage.setTitleTextSize(form.form('get value', 'titleSize'))
    } else {
        form.form('validate field', 'titleSize')
    }
})

buttonContentSizeApply.click(() => {
    if (form.form('is valid', 'contentSize')) {
        settingsStorage.setContentTextSize(form.form('get value', 'contentSize'))
    } else {
        form.form('validate field', 'contentSize')
    }
})

buttonTextColourApply.click(() => {
    if (form.form('is valid', 'textColour')) {
        settingsStorage.setTextColour(form.form('get value', 'textColour'))
    } else {
        form.form('validate field', 'textColour')
    }
})

buttonBackgroundColourApply.click(() => {
    if (form.form('is valid', 'backgroundColour')) {
        settingsStorage.setBackgroundColour(form.form('get value', 'backgroundColour'))
    } else {
        form.form('validate field', 'backgroundColour')
    }
})

buttonLabelBackgroundColourApply.click(() => {
    if (form.form('is valid', 'labelBackgroundColour')) {
        settingsStorage.setLabelBackgroundColour(form.form('get value', 'labelBackgroundColour'))
    } else {
        form.form('validate field', 'labelBackgroundColour')
    }
})

buttonTitleSizeReset.click(() => {
    settingsStorage.resetTitleTextSize()
})

buttonContentSizeReset.click(() => {
    settingsStorage.resetContentTextSize()
})

buttonTextColourReset.click(() => {
    settingsStorage.resetTextColour()
})

buttonBackgroundColourReset.click(() => {
    settingsStorage.resetBackgroundColour()
})

buttonLabelBackgroundColourReset.click(() => {
    settingsStorage.resetLabelBackgroundColour()
})

buttonOpacityReset.click(() => {
    settingsStorage.resetOpacity()
})

sliderTitleSize.slider({
    min: settingsStorage.textSizeMinValue,
    max: settingsStorage.textSizeMaxValue,
}).slider('setting', 'onMove', value => {
    settingsStorage.setTitleTextSize(value)
    form.form('set value', 'titleSize', value)
    form.form('validate field', 'titleSize')
})

sliderContentSize.slider({
    min: settingsStorage.textSizeMinValue,
    max: settingsStorage.textSizeMaxValue,
}).slider('setting', 'onMove', value => {
    settingsStorage.setContentTextSize(value)
    form.form('set value', 'contentSize', value)
    form.form('validate field', 'contentSize')
})

sliderOpacity.slider({
    min: 0,
    max: 1,
    step: 0,
}).slider('setting', 'onMove', value => {
    settingsStorage.setOpacity(value)
    form.form('set value', 'opacity', value)
})

const updateTitleSizeValue = titleTextSize => {
    sliderTitleSize.slider('set value', titleTextSize)
}

const updateContentSizeValue = contentTextSize => {
    sliderContentSize.slider('set value', contentTextSize)
}

const updateTextColourValue = textColour => {
    form.form('set value', 'textColour', textColour)
}

const updateBackgroundColourValue = backgroundColour => {
    form.form('set value', 'backgroundColour', backgroundColour)
}

const updateLabelBackgroundColourValue = labelBackgroundColour => {
    form.form('set value', 'labelBackgroundColour', labelBackgroundColour)
}

const updateSliderOpacity = opacity => {
    sliderOpacity.slider('set value', opacity)
}

export const open = () => {
    modal.modal('show')
}

settingsStorage.titleTextSizeSubject.subscribe(updateTitleSizeValue)
settingsStorage.contentTextSizeSubject.subscribe(updateContentSizeValue)
settingsStorage.textColourSubject.subscribe(updateTextColourValue)
settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColourValue)
settingsStorage.labelBackgroundColourSubject.subscribe(updateLabelBackgroundColourValue)
settingsStorage.opacitySubject.subscribe(updateSliderOpacity)
