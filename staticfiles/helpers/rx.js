const { BehaviorSubject: RxjsBehaviorSubject, skipWhile } = rxjs

export class BehaviorSubject extends RxjsBehaviorSubject {
    constructor(initialValue) {
        super(initialValue)
        return this.pipe(skipWhile(value => value === undefined))
    }
}
