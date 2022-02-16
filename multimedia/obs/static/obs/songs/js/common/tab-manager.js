const tabSelector = '#tab-menu .item'
$(tabSelector).tab()

export const changeTab = name =>
    $(tabSelector).tab('change tab', name)
