import { defineConfig } from 'vitest/config'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/js/setup.js'],
    include: [
      'static/**/*.test.js',
      'multimedia/**/static/**/*.test.js',
      'tests/js/**/*.test.js',
    ],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      reportsDirectory: './coverage-js',
      include: [
        'static/helpers/**/*.js',
        'multimedia/obs/static/**/*.js',
        'multimedia/web/static/**/*.js',
      ],
      exclude: [
        '**/libs/**',
        '**/*.min.js',
        '**/*.test.js',
      ],
    },
  },
  resolve: {
    alias: {
      '@helpers': path.resolve(root, 'static/helpers'),
      '@obs': path.resolve(root, 'multimedia/obs/static/obs'),
      '@web': path.resolve(root, 'multimedia/web/static/web'),
      // App modules import absolute /static/... paths in the browser.
      '/static/helpers': path.resolve(root, 'static/helpers'),
    },
  },
})
