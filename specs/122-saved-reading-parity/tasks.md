# Tasks 122: Saved reading page parity

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepted this Draft.
- [x] Add a browser regression that syncs the saved library and catches the immediate sidebar-open mismatch for a song and empty service.
- [x] Compare saved and server markup across Home, Bible, Kidung, Tata Ibadah, and search routes, including accessible headings, hymn references, and empty actions.
- [x] Align the saved renderer/reconciliation with the server page while preserving offline operation and live sidebar state.
- [x] Verify saved first render, direct server load, and offline sidebar paths for each reading route family; run the focused browser modules against SQLite and PostgreSQL. The existing navigation/offline modules and the new parity module pass separately against PostgreSQL (3 + 21 + 3 tests). A combined PostgreSQL invocation hit a shared test-database lifecycle error, so the successful module runs are the validation evidence.
- [x] Update ITEM-122, board, VERSION, and changelog on this branch.
- [x] Open draft [PR #370](https://github.com/rsmbyk/multimedia-gkps-klender/pull/370) from `fix/122-saved-reading-parity` and record its URL on ITEM-122 and the board.
