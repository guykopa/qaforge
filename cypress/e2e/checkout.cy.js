describe('Checkout Flow', () => {
  beforeEach(() => {
    cy.visit('/products')
    cy.get('[data-cy=add-to-cart]').click()
    cy.get('[data-cy=proceed-to-checkout]').click()
  })

  it('completes checkout with valid card', () => {
    cy.fillAddress('1 Rue de Rivoli', 'Paris', '75001')
    cy.get('[data-cy=card-number]').type('4111111111111111')
    cy.get('[data-cy=confirm-order]').click()
    cy.get('[data-cy=order-success]').should('be.visible')
    cy.get('[data-cy=order-number]').should('not.be.empty')
  })

  it('shows error with declined card', () => {
    cy.fillAddress('10 Rue du Commerce', 'Lyon', '69002')
    cy.get('[data-cy=card-number]').type('4000000000000002')
    cy.get('[data-cy=confirm-order]').click()
    cy.get('[data-cy=order-error]').should('be.visible')
  })
})
