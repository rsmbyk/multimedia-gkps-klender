const defaultSelector = '.ui.menu .item'

let activeTab

export const init = (selector=null) => {
    $(selector !== null ? selector : defaultSelector).tab('setting', 'onVisible', (tabPath) => {
        activeTab = tabPath
    })
}

export const changeTab = (name, selector=null) =>
    $(selector !== null ? selector : defaultSelector).tab('change tab', name)

export const getActiveTab = () => {
    return activeTab
}
