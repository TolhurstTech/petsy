const editButtons = document.getElementsByClassName("btn-edit");
const reviewRating = document.getElementById("id_ratings");
const reviewText = document.getElementById("id_content");
const reviewForm = document.getElementById("reviewForm");
const submitButton = document.getElementById("submitButton");
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

/**
* Initializes edit functionality for the provided edit buttons.
* For each button in the `editButtons` collection:
* - Retrieves the associated reviews's ID upon click.
* - Fetches the content of the corresponding review.
* - Fetches the review rating
* - Populates the `reviewText` input/textarea with
*   the review's content for editing.
* - Sets reviewRatings dropdown to the rating stored in the review
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_review/{reviewId}` endpoint.
*/
for (let button of editButtons) {
  button.addEventListener("click", (e) => {
    let reviewId = e.target.getAttribute("data-review_id");
    let reviewContent = document.getElementById(`review${reviewId}`).innerText;
    let reviewRatingData = document.querySelector("#rating");
    let reviewRatingContent = reviewRatingData.dataset.rating;
    reviewText.value = reviewContent;
    reviewRating.selectedIndex = (reviewRatingContent - 1);
    submitButton.innerText = "Update";
    reviewForm.setAttribute("action", `edit_review/${reviewId}`);
  });
}

/**
* Initializes deletion functionality for the provided delete buttons.
* For each button in the `deleteButtons` collection:
* - Retrieves the associated review's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the
* deletion endpoint for the specific review.
* - Displays a confirmation modal (`deleteModal`) to prompt
* the user for confirmation before deletion.
*/
for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      let reviewId = e.target.getAttribute("data-review_id");
      deleteConfirm.href = `delete_review/${reviewId}`;
      deleteModal.show();
    });
}