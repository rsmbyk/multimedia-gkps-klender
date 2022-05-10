const buttonFocusIndicator = $('#button-focus-indicator')

const onFocus = colourClass => {
    buttonFocusIndicator.addClass(colourClass)
}

const onBlur = colourClass => {
    buttonFocusIndicator.removeClass(colourClass)
}

export const registerFocusChange = colourClass => {
    window.onfocus = () => { onFocus(colourClass) }
    window.onblur = () => { onBlur(colourClass) }

    if (document.hasFocus()) {
        onFocus(colourClass)
    } else {
        onBlur(colourClass)
    }
}
