describe('Shopping Cart', () => {
  beforeEach(() => {
    cy.visit('/products')
  })

  it('adds item to cart and updates total', () => {
    cy.get('[data-cy=add-to-cart]').click()
    cy.get('[data-cy=cart-total]')
      .should('be.visible')
      .and('not.contain', '€0.00')
  })

  it('applies discount code and reduces total', () => {
    const parseAmount = (text) => parseFloat(text.replace('€', '').trim())

    cy.get('[data-cy=add-to-cart]').click()
    cy.get('[data-cy=cart-total]').invoke('text').then((originalText) => {
      const originalTotal = parseAmount(originalText)
      cy.get('[data-cy=discount-input]').type('SAVE10')
      cy.get('[data-cy=apply-discount]').click()
      cy.get('[data-cy=cart-total]').invoke('text').then((discountedText) => {
        expect(parseAmount(discountedText)).to.be.lessThan(originalTotal)
      })
    })
  })
})
