const { BehaviorSubject: RxjsBehaviorSubject, skipWhile } = rxjs

const attachSubject = (subject, observable) => {
    observable.next = (...args) => subject.next(...args)
    observable.getValue = () => subject.getValue()

    const originalPipe = observable.pipe.bind(observable)
    observable.pipe = (...operators) => attachSubject(subject, originalPipe(...operators))

    return observable
}

export class BehaviorSubject extends RxjsBehaviorSubject {
    constructor(initialValue) {
        super(initialValue)
        return attachSubject(
            this,
            RxjsBehaviorSubject.prototype.pipe.call(this, skipWhile(value => value === undefined)),
        )
    }

    pipe(...operators) {
        return attachSubject(this, RxjsBehaviorSubject.prototype.pipe.apply(this, operators))
    }
}
