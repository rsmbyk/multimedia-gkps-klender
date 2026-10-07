/**
 * Pure helpers for web tatib item reorder payloads.
 */
export function buildTatibReorderRequestData(itemsOrder) {
  return {
    items: itemsOrder.map((item, index) => ({
      item: item.id,
      order_number: index + 1,
    })),
  }
}
