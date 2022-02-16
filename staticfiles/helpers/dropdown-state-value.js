class DropdownStateValue {
    constructor(name, selector, localStorageKey) {
        this.name = name
        this.dropdown = $(selector)
        this.localStorage = new LocalStorageHelper(localStorageKey)
    }

    get selectedValue() {
        return this.dropdown.dropdown('get value')
    }

    get defaultValue() {
        return this.dropdown.find('.menu .item').data('value')
    }

    setValue(value) {
        this.dropdown.dropdown('set selected', value)
        this.localStorage.setValue(value)
    }

    init(settings, onChange, loadPreviousValue) {
        this.dropdown.dropdown(settings)

        this.dropdown.dropdown('setting', 'onChange', value => {
            if (onChange !== undefined) onChange(value)
            this.localStorage.setValue(value)
        })

        if (loadPreviousValue && this.localStorage.value) this.setValue(this.localStorage.value)
        else this.setValue(this.defaultValue)
    }
}

class SearchDropdownStateValue extends DropdownStateValue {
    constructor(name, selector, subMenuSelector, localStorageKey) {
        super(name, selector, localStorageKey);
        this.subMenu = $(subMenuSelector)
    }

    init(values, onChange, loadPreviousValue) {
        this.subMenu.empty()
        values.forEach(item => this.subMenu.append(item))

        const settings = {
            hideDividers: 'empty',
            fullTextSearch: true
        }

        super.init(settings, onChange, loadPreviousValue)
    }
}
