const editButtons = document.getElementsByClassName("btn-edit");
const reviewRating = document.querySelector("#id_ratings");
//const reviewRating = document.getElementById('id_ratings')
const reviewText = document.getElementById("id_content");
const reviewForm = document.getElementById("reviewForm");
const submitButton = document.getElementById("submitButton");

/**
* Initializes edit functionality for the provided edit buttons.
* 
* For each button in the `editButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Fetches the content of the corresponding comment.
* - Populates the `commentText` input/textarea with the comment's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
*/
for (let button of editButtons) {
  button.addEventListener("click", (e) => {
    let reviewId = e.target.getAttribute("data-review_id");
    let reviewContent = document.getElementById(`review${reviewId}`).innerText;
    let reviewRatingContent = reviewRating.dataset.rating;
    console.log(reviewRatingContent);
    reviewText.value = reviewContent;
    document.getElementById('id_ratings').selectIndex = (reviewRatingContent + 1);
    submitButton.innerText = "Update";
    reviewForm.setAttribute("action", `edit_review/${reviewId}`);
  });
}