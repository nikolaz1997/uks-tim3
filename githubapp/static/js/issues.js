var closedIssueButton = document.querySelector("#closed-issue-button");
var openedIssueButton = document.querySelector("#opened-issue-button");
var opened_issues = document.getElementById("opened-issues");
var closed_issues = document.getElementById("closed-issues");

closedIssueButton.addEventListener("click", function (e) {
  e.preventDefault();
  closed_issues.style.display = "block";
  closedIssueButton.classList.add("active");
  opened_issues.style.display = "none";
  openedIssueButton.classList.remove("active");
});

openedIssueButton.addEventListener("click", function (e) {
  e.preventDefault();
  opened_issues.style.display = "block";
  openedIssueButton.classList.add("active");
  closed_issues.style.display = "none";
  closedIssueButton.classList.remove("active");
});

document
  .querySelector("input[name='search-issues']")
  .addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      document.querySelector("form").submit();
    }
  });
