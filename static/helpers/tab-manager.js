const defaultSelector = '.ui.menu .item'

let activeTab

const resolveSelector = (selector) => selector !== null ? selector : defaultSelector

export const init = (selector = null) => {
    const resolvedSelector = resolveSelector(selector)

    $(resolvedSelector).tab('setting', 'onVisible', (tabPath) => {
        activeTab = tabPath
    })

    const activeItem = $(resolvedSelector).find('.item.active').first()
    if (activeItem.length > 0) {
        activeTab = activeItem.attr('data-tab')
    }
}

export const changeTab = (name, selector = null) =>
    $(resolveSelector(selector)).tab('change tab', name)

export const getActiveTab = () => activeTab
