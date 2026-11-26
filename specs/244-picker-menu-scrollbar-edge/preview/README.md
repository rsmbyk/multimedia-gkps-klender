# Preview — picker popout scrollbar edge

**Shape**: live. The change is applied in this worktree's `static/styles/design/components.css` and
served from the real dev server — no injected styles, no static copy.

**URL**: `http://127.0.0.1:8778/` (dev server process cwd
`/home/rsmbyk/Projects/multimedia-gkps-klender-244`; confirm with
`ss -ltnp | grep 8778` and `readlink /proc/<pid>/cwd` before trusting the port).

## How to reach the states

1. Open `/` and click the **Tata Ibadah** rail tile — do not use a deep link.
2. Click the first service (`Ibadah Pace Probe` on the local database).
3. Hover the add bar at the top of the reading stage, then click **+ Passage**.
4. Click the **Book** search field: the menu holds 66 books and overflows. The bar is at its right edge.
5. Choose a book (e.g. Kejadian) to enable **Chapter**, **From verse** and **To verse**. Each button
   opens a menu with its own filter and an overflowing option list.
6. Type in a filter to narrow the list; choose **Obaja** as the book to get a one-option Chapter
   menu with no bar and no reserved lane.
7. Switch the theme with the rail's theme button to check the dark bar; make the window short to
   make the menu flip above its trigger.

## Frozen measurements

At 1440×900, dpr 1, light theme, base → slice CSS in the same live path:

| Surface | Menu right / bottom | Scrollport right / bottom before | Scrollport right / bottom after |
| --- | --- | --- | --- |
| Book | 938 / 892 | 929 / 883 | 937 / 891 |
| Chapter | 938 / 892 | 929 / 883 | 937 / 891 |
| From verse | 715 / 892 | 706 / 883 | 714 / 891 |
| Chapter, Obaja (no overflow) | 938 / 597.3 | — | 937 / 596.3 |

The first book option stays x 511→929, y 464.1→503.1; the chapter filter stays x 511→929,
y 510.1→548.1. The scrollbar remains the spec 087 5px `--scroll-thumb` bar.

## Verification probe

`python specs/244-picker-menu-scrollbar-edge/preview/measure.py 8778 after` walks the path
above and prints the menu/scrollport boxes for Book, Chapter and From verse. It lives beside the
pack (a scratch copy is temporary and would be pruned); a product E2E is written during Implement.
