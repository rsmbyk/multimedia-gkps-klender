import * as settingsStorage from '../common/settings-storage.js'

const form = $('#project-settings-form')

const buttonTitleTextColourApply = $('#project-settings-form-title-text-colour-button-apply')
const buttonTitleTextColourReset = $('#project-settings-form-title-text-colour-button-reset')

const buttonContentTextColourApply = $('#project-settings-form-content-text-colour-button-apply')
const buttonContentTextColourReset = $('#project-settings-form-content-text-colour-button-reset')

const buttonBackgroundColourApply = $('#project-settings-form-background-colour-button-apply')
const buttonBackgroundColourReset = $('#project-settings-form-background-colour-button-reset')

form.form({
    fields: {
        titleTextColour: {
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
        contentTextColour: {
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
    },
    inline: true,
})

buttonTitleTextColourApply.click(() => {
    if (form.form('is valid', 'titleTextColour')) {
        settingsStorage.setTitleTextColour(form.form('get value', 'titleTextColour'))
    } else {
        form.form('validate field', 'titleTextColour')
    }
})

buttonContentTextColourApply.click(() => {
    if (form.form('is valid', 'contentTextColour')) {
        settingsStorage.setContentTextColour(form.form('get value', 'contentTextColour'))
    } else {
        form.form('validate field', 'contentTextColour')
    }
})

buttonBackgroundColourApply.click(() => {
    if (form.form('is valid', 'backgroundColour')) {
        settingsStorage.setBackgroundColour(form.form('get value', 'backgroundColour'))
    } else {
        form.form('validate field', 'backgroundColour')
    }
})

buttonTitleTextColourReset.click(() => {
    settingsStorage.resetTitleTextColour()
    updateTitleTextColourValue(settingsStorage.defaultTitleTextColour)
})

buttonContentTextColourReset.click(() => {
    settingsStorage.resetContentTextColour()
    updateContentTextColourValue(settingsStorage.defaultContentTextColour)
})

buttonBackgroundColourReset.click(() => {
    settingsStorage.resetBackgroundColour()
    updateBackgroundColourValue(settingsStorage.defaultBackgroundColour)
})

const updateTitleTextColourValue = titleTextColour => {
    form.form('set value', 'titleTextColour', titleTextColour)
}

const updateContentTextColourValue = contentTextColour => {
    form.form('set value', 'contentTextColour', contentTextColour)
}

const updateBackgroundColourValue = backgroundColour => {
    form.form('set value', 'backgroundColour', backgroundColour)
}

settingsStorage.titleTextColourSubject.subscribe(updateTitleTextColourValue)
settingsStorage.contentTextColourSubject.subscribe(updateContentTextColourValue)
settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColourValue)
