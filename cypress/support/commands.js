// Custom Cypress commands shared across all test files

/**
 * Fill the delivery address form on the checkout page.
 * @param {string} street - Street address
 * @param {string} city - City name
 * @param {string} zipCode - Postal code
 */
Cypress.Commands.add('fillAddress', (street, city, zipCode) => {
  cy.get('[data-cy=street]').clear().type(street)
  cy.get('[data-cy=city]').clear().type(city)
  cy.get('[data-cy=zip-code]').clear().type(zipCode)
})
