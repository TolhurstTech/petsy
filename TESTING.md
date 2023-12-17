# Testing

I deployed my app early so that I could test every feature in local and deployment stages as I built them and to save me from as many nasty surprises near the end of the project as possible. 

Upon completion of the project I developed these manual test to make sure the project was up to MVP standards and that everything worked as planned.

### Manual Testing


#### Non-logged in User

| Page         | Test                        | Expected outcome                                            | Pass/Fail   |
|--------------|-----------------------------|-------------------------------------------------------------|-------------|
| Home Page | Click the logo | Should navigate to the homepage | Pass        |
| Home Page | Click every navigation link | Should open the correct page and set the current page link as active with aria label | Pass|
| Home Page | Click home or logo | Displays a list of all products correctly, paginated by 6 | Pass |
| Home Page | Load home page | Navigation bar shows options to log in or register when not logged in | Pass |
| Home Page | Click any product on the home page | Opens it's product detail page | Pass |
| Home Page | Load home page | "Log in to +" button shows on products for non-logged in user | Pass |
| Home Page | Click "Log in to +" buttons |"Log in to +" buttons take the user to the login page | Pass |
| Home Page | Click the Next and Back buttons | Next and Back buttons display and show next and previous pages when clicked | Pass |


#### Logged in User
