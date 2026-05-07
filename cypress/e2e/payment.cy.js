describe('Payment Processing', () => {
  beforeEach(() => {
    cy.visit('/products')
    cy.get('[data-cy=add-to-cart]').click()
    cy.get('[data-cy=proceed-to-checkout]').click()
    cy.fillAddress('5 Avenue Montaigne', 'Paris', '75008')
  })

  it('refund option is available after successful payment', () => {
    cy.get('[data-cy=card-number]').type('4111111111111111')
    cy.get('[data-cy=confirm-order]').click()
    cy.get('[data-cy=order-success]').should('be.visible')
    cy.get('[data-cy=refund-btn]').should('be.visible')
  })
})
