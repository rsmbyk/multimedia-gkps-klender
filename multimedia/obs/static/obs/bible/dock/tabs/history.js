import * as doms from '/static/helpers/doms.js'

import * as historyManager from '../common/history-manager.js'

import * as browseTab from './browse.js'
import * as displayTab from './display.js'

const chapterList = $('#history-chapter-list')

const containerChapterList = $('#history-container-chapter-list')
const viewEmpty = $('#history-view-empty')

const displayChapterList = () => {
    viewEmpty.hide()
    containerChapterList.show()
}

const displayEmptyView = () => {
    containerChapterList.hide()
    viewEmpty.show()
}

const createChapterListItem = ({ translation, chapterNumber, verses, verseNumber }) => {
    const item = doms.createDOMFromJSON({
        tag: 'div',
        classList: ['item'],
        children: [
            {
                tag: 'div',
                classList: ['content'],
                children: [
                    {
                        tag: 'div',
                        classList: ['header'],
                        innerText: `${translation.translation} ${chapterNumber} : ${verseNumber}`,
                    },
                ],
            },
        ],
    })

    item.click(() => {
        displayTab.display(translation, chapterNumber, verses, verseNumber)
        browseTab.open(translation, chapterNumber, verses)
        displayTab.navigateTo()
    })

    return item
}

const updateChapterList = history => {
    chapterList.empty()
    chapterList.append(...history.map(createChapterListItem))

    if (history.length === 0) displayEmptyView()
    else displayChapterList()
}

historyManager.historySubject.subscribe(updateChapterList)
