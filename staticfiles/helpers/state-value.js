import { LocalStorageHelper } from '/static/helpers/local-storage.js'

export class StateValue {
    constructor(key) {
        this.localStorage = new LocalStorageHelper(key)
    }

    get currentValue() {
        throw 'Must implement \'currentValue\''
    }

    get defaultValue() {
        throw 'Must implement \'defaultValue\''
    }

    get savedValue() {
        return this.localStorage.value
    }

    setValue = value => {
        this.setInternalValue(value)
        this.saveValue(value)
    }

    setInternalValue(value) {
        throw 'Must implement \'setInternalValue\''
    }

    saveValue(value) {
        this.localStorage.setValue(value)
    }

    init(loadSavedValue) {
        if (loadSavedValue && this.savedValue) this.setInternalValue(this.savedValue)
        else this.setValue(this.defaultValue)
    }
}

export class DropdownStateValue extends StateValue {
    constructor(key, dropdown) {
        super(key)
        this.dropdown = dropdown
        this.lastValue = undefined
    }

    get currentValue() {
        return this.dropdown.dropdown('get value')
    }

    get defaultValue() {
        return this.dropdown.find('.menu .item').data('value')
    }

    setInternalValue(value) {
        this.dropdown.dropdown('set selected', value)
    }

    init(onChange, loadSavedValue) {
        this.dropdown.dropdown('setting', 'onChange', value => {
            if (value === this.lastValue)
                return

            this.lastValue = value
            if (onChange instanceof Function) onChange(value)
            this.saveValue(value)
        })

        super.init(loadSavedValue)
    }
}
