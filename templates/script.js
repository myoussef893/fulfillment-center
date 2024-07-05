const button = document.getElementsByClassName("btn btn-success");

button.addEventListener("click", () => {
  button.classList.add("added");
  button.textContent = "Item Added";
});
