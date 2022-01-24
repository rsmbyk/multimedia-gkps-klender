class LocalStorageHelper {
    constructor(name) {
        this.name = name
    }

    get value() {
        return localStorage.getItem(this.name)
    }

    setValue(value) {
        localStorage.setItem(this.name, value)
    }
}
