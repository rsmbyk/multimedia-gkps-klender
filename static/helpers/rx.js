const { BehaviorSubject: RxjsBehaviorSubject, skipWhile } = rxjs

export class BehaviorSubject extends RxjsBehaviorSubject {
    constructor(initialValue) {
        super(initialValue)
    }

    subscribe(...args) {
        return super.pipe(skipWhile(value => value === undefined)).subscribe(...args)
    }
}
