export class ManualToggleButton {
    constructor(btnActive, btnInactive, onActive, onInactive,) {
        this.btnActive = $(btnActive)
        this.btnInactive = $(btnInactive)
        this.onActive = onActive
        this.onInactive = onInactive

        this.isActive = false
        this.isShown = true
        this.setInactive()
    }

    setActive() {
        this.btnInactive.hide()
        if (this.isShown) this.btnActive.show()

        if (this.onActive instanceof Function)
            this.onActive()

        this.isActive = true
    }

    setInactive() {
        this.btnActive.hide()
        if (this.isShown) this.btnInactive.show()

        if (this.onInactive instanceof Function)
            this.onInactive()

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
