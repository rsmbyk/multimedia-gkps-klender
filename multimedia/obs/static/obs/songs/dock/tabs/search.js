import * as doms from '/static/helpers/doms.js'

import * as songDetailModal from '../../dock/modals/song-detail.js'

const form = $('#search-form')

const verseList = $('#search-verse-list')
const buttonLoadMore = $('#search-button-load-more')

const viewEmpty = $('#search-view-empty')
const viewError = $('#search-view-error')
const containerVerseList = $('#search-container-verse-list')
const containerButtonLoadMore = $('#search-container-button-load-more')

let nextUrl

const showLoader = () => {
    form.find('.input').addClass('loading disabled')
    buttonLoadMore.addClass('loading disabled')
}

const hideLoader = () => {
    form.find('.input').removeClass('loading disabled')
    buttonLoadMore.removeClass('loading disabled')
}

const displayPlaceholder = () => {
    containerVerseList.hide()
    containerButtonLoadMore.hide()
    viewEmpty.hide()
    viewError.hide()
}

const displayVerseList = () => {
    containerVerseList.show()
}

const displayEmptyView = () => {
    viewEmpty.show()
}

const displayErrorView = e => {
    console.log(e)
    viewError.show()
}

const createSearchResultItem = ({ song: { id: songId, book, title, number: songNumber, sub_number, is_untitled }, number: verseNumber, lyric }) => {
    const songBookNumber = book.is_hymn_book ? `${book.short_name} ${songNumber}${sub_number} : ${verseNumber} ` : ''
    const songTitle = book.is_hymn_book ? `(${title})` : title
    const songUntitledMarker = is_untitled ? ' *' : ''

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
                        innerText: songBookNumber + songTitle + songUntitledMarker,
                    },
                    {
                        tag: 'div',
                        classList: ['description'],
                        innerText: lyric,
                    },
                ],
            },
        ],
    })

    /*
     code taken from https://stackoverflow.com/a/19049457/5447454
     to make texts ellipsis at certain number of lines.
     */
    const description = item.find('.description')
    description.css('text-overflow', 'ellipsis')
    description.css('overflow', 'hidden')
    description.css('display', '-webkit-box')
    description.css('-webkit-line-clamp', '3')
    description.css('-webkit-box-orient', 'vertical')

    item.click(() => {
        songDetailModal.open(songId)
    })

    item.hover(() => {
        description.css('-webkit-line-clamp', '')
    }, () => {
        description.css('-webkit-line-clamp', '3')
    })

    return item
}

const updateSearchResult = searchResult => {
    verseList.append(...searchResult.results.map(createSearchResultItem))

    hideLoader()

    nextUrl = searchResult.next

    if (searchResult.next === null) containerButtonLoadMore.hide()
    else containerButtonLoadMore.show()

    if (searchResult.count === 0) displayEmptyView()
    else displayVerseList()
}

const retrieveSearchResult = () => {
    showLoader()

    axios.get(nextUrl)
        .then(({ data: searchResults }) => updateSearchResult(searchResults))
        .catch(displayErrorView)
}

buttonLoadMore.click(retrieveSearchResult)

form.form({
    fields: {
        q: ['empty', 'minLength[3]'],
    },
    inline: true,
    on: 'submit',
})

form.submit(e => {
    e.preventDefault()

    if (form.form('is valid')) {
        const { q } = form.form('get values')

        displayPlaceholder()
        verseList.empty()
        nextUrl = `/api/search/songs?q=${q}`
        retrieveSearchResult()
    }
    else {
        form.form('validate form')
    }
})
