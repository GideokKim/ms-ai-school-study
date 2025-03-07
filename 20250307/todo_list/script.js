const $inputTodo = document.getElementById("input-todo");
const $btnAdd = document.getElementById("btn-add");

let todoList = [];

function addTodo() {
  const todo = $inputTodo.value;
  if (todo === "") return;

  todoList.push({
    id: Date.now(),
    todoText: todo,
    isComplete: false,
  });

  renderTodoList();

  saveWebStorage();

  $inputTodo.value = "";
}

function renderTodoList() {
  let $ol = document.getElementById("todo-list");
  $ol.innerHTML = "";
  let $li, $input, $span, $button, $spanText, $buttonText;
  for (idx in todoList) {
    // 요소노드
    $li = document.createElement("li");
    $input = document.createElement("input");
    $span = document.createElement("span");
    $button = document.createElement("button");
    // 요소 속성
    $li.setAttribute("class", "todo-item");
    $input.setAttribute("type", "checkbox");
    $button.setAttribute("class", "delete-btn");
    $button.setAttribute("onclick", `deleteTodo(${todoList[idx].id})`);
    $input.setAttribute("onchange", `toggleTodo(${todoList[idx].id})`);

    if (todoList[idx].isComplete) {
      $input.setAttribute("checked", "checked");
      $span.setAttribute("class", "completed");
    }

    //텍스트노드
    $spanText = document.createTextNode(`${todoList[idx].todoText}`);
    $buttonText = document.createTextNode("삭제");

    // 노드 구성
    $ol.appendChild($li);
    $li.appendChild($input);
    $li.appendChild($span);
    $li.appendChild($button);
    $span.appendChild($spanText);
    $button.appendChild($buttonText);
  }
}

function saveWebStorage() {
  localStorage.setItem("todoList", JSON.stringify(todoList));
}

function loadWebStorage() {
  const todoList = localStorage.getItem("todoList");
  if (todoList) {
    todoList = JSON.parse(todoList);
  }
  renderTodoList();
}

function deleteTodo(id) {
  todoList = todoList.filter((todo) => todo.id !== id);
  renderTodoList();
  saveWebStorage();
}

function toggleTodo(id) {
  for (idx in todoList) {
    if (todoList[idx].id === id) {
      todoList[idx].isComplete = !todoList[idx].isComplete;
      break;
    }
  }

  saveWebStorage();
  renderTodoList();
}

$inputTodo.addEventListener("keyup", (e) => {
  if (e.key === "Enter") addTodo();
});

$btnAdd.addEventListener("click", addTodo);
