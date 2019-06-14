const addTypesPreformanceHandler = type => {
  const addButton = document.querySelector(`.add_${type}_button`);
  const inputForm = document.querySelector(`.add_${type}_wrapper`);
  const cancelButton = document.querySelector(`.cancel_add_${type}`);
  const toggleAddTask = () => {
    inputForm.classList.toggle("hidden");
    addButton.classList.toggle("hidden");
  };
  addButton && addButton.addEventListener("click", toggleAddTask);
  cancelButton && cancelButton.addEventListener("click", toggleAddTask);
};

const hoverItem = type => {
  const container = document.querySelector(`.${type}_container`);
  let form, element;
  container &&
    container.addEventListener("click", e => {
      if (
        !form &&
        !element &&
        e.target.classList.contains(`${type}_edit_menu`)
      ) {
        form = e.target.parentElement.nextElementSibling;
        element = e.target.parentElement;
        form.classList.toggle("hidden");
        element.classList.toggle("hidden");
      }
      if (e.target.classList.contains(`cancel_edit_${type}`)) {
        form.classList.toggle("hidden");
        element.classList.toggle("hidden");
        form = null;
        element = null;
      }
    });
};

const createListeners = () => {
  addTypesPreformanceHandler("task");
  addTypesPreformanceHandler("project");
  hoverItem("projects");
  hoverItem("tasks");
};

createListeners();
