/**
 * Vitest setup for OBS / web modules that expect browser globals.
 */
import * as rxjs from 'rxjs'

globalThis.rxjs = rxjs
