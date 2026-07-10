import { describe, expect, it } from 'vitest'
import { buildTatibReorderRequestData } from './reorder.js'

describe('buildTatibReorderRequestData', () => {
  it('maps list order to 1-based order_number payloads', () => {
    expect(
      buildTatibReorderRequestData([{ id: 10 }, { id: 20 }, { id: 30 }]),
    ).toEqual({
      items: [
        { item: 10, order_number: 1 },
        { item: 20, order_number: 2 },
        { item: 30, order_number: 3 },
      ],
    })
  })
})
