import * as bookmarkManager from '../common/bookmark-manager.js'
import {bookmark} from "../common/bookmark-manager.js";

const modal = $('#modal-paste')

const form = $('#modal-paste-form')

const buttonPaste = $('#modal-paste-button-paste')
const buttonCancel = $('#modal-paste-button-cancel')

const showLoader = () => {
    form.addClass('loading')
    buttonPaste.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    form.removeClass('loading')
    buttonPaste.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const displayLyric = () => {
    form.removeClass('error')

    if (form.form('is valid')) {
        const { lyric } = form.form('get values')

        showLoader()
        bookmarkManager.activateSingleBookmarkItem({
            is_hymn_book: false,
        }, {
            title: '[NO_TITLE]',
            is_untitled: true,
        }, [
            {
                number: 1,
                lyric: lyric,
            },
        ])
        modal.modal('hide')
    }
    else {
        form.form('validate form')
    }
}

const checkQuickPasteInBookmark = () => {
    if (bookmarkManager.bookmarkItems !== null && bookmarkManager.bookmarkItems.length === 1)
        if (bookmarkManager.bookmarkItems[0].song_info.title === '[NO_TITLE]')
            form.form('set value', 'lyric', bookmarkManager.bookmarkItems[0].verse_info[0].lyric)
}

export const open = () => {
    checkQuickPasteInBookmark()
    hideLoader()
    modal.modal('show')
}

modal.modal({
    closable: false,
    onHide: function() {
        form.form('clear')
    },
    onApprove: function() {
        displayLyric()
        return false
    },
})

form.form({
    fields: {
        lyric: ['empty'],
    },
    inline: true,
    on: 'change',
})
