# Testing

I deployed my app early so that I could test every feature in local and deployment stages as I built them and to save me from as many nasty surprises near the end of the project as possible. 

Upon completion of the project I developed these manual test to make sure the project was up to MVP standards and that everything worked as planned.

### Manual Testing


#### Non-logged in User

| Page         | Test                        | Expected outcome                                            | Pass/Fail   |
|--------------|-----------------------------|-------------------------------------------------------------|-------------|
| Home Page | Click the logo | Should navigate to the homepage | Pass        |
| Home Page | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Home Page | Click home or logo | Displays a list of all products correctly within the page, paginated by 6 | Pass |
| Home Page | Load home page | Navigation bar shows options to log in or register when not logged in | Pass |
| Home Page | Click any product on the home page | Opens it's product detail page | Pass |
| Home Page | Load home page | "Log in to +" button shows on products for non-logged in user | Pass |
| Home Page | Click "Log in to +" buttons |"Log in to +" buttons take the user to the login page | Pass |
| Home Page | Click the Next and Back buttons | Next and Back buttons display and show next and previous pages when clicked | Pass |
| Product Detail |  Click the logo | Should navigate to the homepage | Pass        |
| Product Detail | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Product Detail | Load page | Should load search box, product detail content, and product reviews area | Pass |
| Product Detail | Load page | "Log in to +" button shows for non-logged in user | Pass |
| Product Detail | Load page | See's approved reviews below product and prompted to log in to leave a review | Pass |
| Product Detail |  Click "Log in to +" button | Opens log in page| Pass|
| Login | Click the logo | Should navigate to the homepage | Pass        |
| Login | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Login | Page loads | Should see a properly styled login form | Pass |
| Login | Fill out form incorrectly | Form validation stops incorrect entry and submission | Pass |
| Login | Login as both types of users | Logs in successfuly and redirects back to storefront | Pass |
| Login | Login as both types of users | Displays a message that the user is now logged in | Pass |
| Login | Login with non-existant user | Hints user or password might be wrong | Pass |
| Login | Login with incorrect password | Hints user or password might be wrong | Pass |
| Cart | Load Page | Displays an empty cart that cant be edited | Pass |
| Cart | Click the logo | Should navigate to the homepage | Pass        |
| Cart | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Checkout | Click the logo | Should navigate to the homepage | Pass        |
| Checkout | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Checkout | Load Page | Displays an empty checkout | Pass |
| Checkout | Enter address | Doesn't break the site | Pass but with console errors|

#### Logged in User
| Page         | Test                        | Expected outcome                                            | Pass/Fail   |
|--------------|-----------------------------|-------------------------------------------------------------|-------------|
| Home Page | Click the logo | Should navigate to the homepage | Pass        |
| Home Page | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Home Page | Click home or logo | Displays a list of all products correctly within the page, paginated by 6 | Pass |
| Home Page | Load home page | Navigation bar shows a user greeting and a logout link | Pass |
| Home Page | Click any product on the home page | Opens it's product detail page | Pass |
| Home Page | Load home page | "Add to cart" button shows on products | Pass |
| Home Page | Click "Add to Cart" buttons |"Add to Cart" buttons add the product to the cart and the cart total updates | Pass |
| Home Page | Click the Next and Back buttons | Next and Back buttons display and show next and previous pages when clicked | Pass |
| Product Detail |  Click the logo | Should navigate to the homepage | Pass        |
| Product Detail | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Product Detail | Load page | Should load search box, product detail content, and product reviews area | Pass |
| Product Detail | Load page | "Add to Cart" button shows for product | Pass |
| Product Detail | Load page | "Add to Cart" button adds product to cart and updates cart total in navbar| Pass |
| Product Detail | Load page | See's approved reviews below product | Pass |
| Product Detail | Load page | See's a form to leave reviews below product | Pass |
| Product Detail | Load page | Can see delete and edit buttons on own reviews | Pass |
| Product Detail | Load page | Can see own reviews awaiting review | Pass |
| Product Detail | Click edit button | Opens review in review form to be edited | Pass |
| Product Detail | Click delete button | Opens model to double check deletion | Pass |
| Product Detail | Click delete button in Modal | Review is deleted | Pass |
| Product Detail | Click delete button in Modal | User is notified their review was deleted | Pass |
| Product Detail | Submit a review | User is notified review has been submitted for approval and it appears below the article for the user greyed out | Pass |
| Product Detail | Edit a Review | User is notified the review has been updated and the updated review appears below the article in the same place | Pass |
| Logout |  Click the logo | Should navigate to the homepage | Pass        |
| Logout | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Logout | Page loads | Should see a properly styled logout confirmation form | Pass |
| Logout | Click Sign Out | Redirect back to home page with a notification the user is now logged out | Pass |
| Cart | Load Page | Displays items user added to cart with correct quantities and totals | Pass |
| Cart |  Click the logo | Should navigate to the homepage | Pass        |
| Cart | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Cart | Click up arrows on every product multiple times | Total increases for each product inline with clicks | Pass |
| Cart | Click down arrows on every product multiple times | Total decreases for each product inline with clicks | Pass |
| Cart | Click down arrows on products with qty of 1 | Item is removed from the cart | Pass |
| Cart | Click Checkout button | Takes you to the checkout with you current cart as the order summary | Pass |
| Checkout | Submit Shipping details | Submit button disappears and payment button appears | Pass but user names aren't being stored properly |
| Checkout | Click payment button | Spoofed payment gives alert transaction is complete | Pass |
| Checkout | Click alert OK button | User is returned to storefront with a fresh cart with a total of 0 and no items | Pass |

## Problems Found
I found during testing that first and last names weren't actually being saved to the database during sign up and therefore weren't being passed to the shipping address form correctly.
I currently don't have time to fix this bug properly but I removed the code to hide email and name fields for logged in users to allow the name to still be captured and saved with the address.

# Responsivity
Site was tested at all bootstrap default breakpoints and appears to work as it should. I set up my media queries to match Bootstrap breakpoints to keep everything uniform, too.

# Browser Compatibility
The site has been tested in Chrome, Microsoft Edge, Chrome for Android and Android browser.

