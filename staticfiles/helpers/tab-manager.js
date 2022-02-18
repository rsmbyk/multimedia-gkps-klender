const TabManager = () => {
    const tabSelector = '#tab-menu.ui.menu .item'

    const initialize = () =>
        $(tabSelector).tab()

    const changeTab = (name) =>
        $(tabSelector).tab('change tab', name)

    return {
        initialize,
        changeTab,
    }
}
