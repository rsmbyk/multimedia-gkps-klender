const defaultSelector = '.ui.menu .item'

export const init = (selector=null) => {
    $(selector !== null ? selector : defaultSelector).tab()
}

export const changeTab = (name, selector=null) =>
    $(selector !== null ? selector : defaultSelector).tab('change tab', name)
