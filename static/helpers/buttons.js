export class ManualToggleButton {
    constructor(btnActive, btnInactive, onActive, onInactive,) {
        this.btnActive = $(btnActive)
        this.btnInactive = $(btnInactive)
        this.onActive = onActive
        this.onInactive = onInactive

        this.isActive = false
        this.isShown = true
        this.setInactive(false, true)
    }

    setActive(skipToggleAction) {
        if (this.isActive) {
            return
        }

        if (!skipToggleAction && this.onActive instanceof Function && this.onActive() === false)
            return

        this.btnInactive.hide()
        if (this.isShown) this.btnActive.show()
        this.isActive = true
    }

    setInactive(skipToggleAction, init) {
        if (!this.isActive && !init) {
            return
        }

        if (!skipToggleAction && this.onInactive instanceof Function && this.onInactive() === true)
            return

        this.btnActive.hide()
        if (this.isShown) this.btnInactive.show()
        this.isActive = false
    }

    show() {
        if (this.isActive) this.btnActive.show()
        else this.btnInactive.show()
        this.isShown = true
    }

    hide() {
        this.btnActive.hide()
        this.btnInactive.hide()
        this.isShown = false
    }
}

export class ToggleButton extends ManualToggleButton {
    constructor(btnActive, btnInactive, onActive, onInactive,) {
        super(btnActive, btnInactive, onActive, onInactive);
        this.btnActive.click(() => this.setInactive())
        this.btnInactive.click(() => this.setActive())
    }
}
