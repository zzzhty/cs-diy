(function () {
  function answerQuiz(button) {
    var quiz = button.closest("[data-quiz]");
    if (!quiz || button.disabled) {
      return;
    }

    var answer = quiz.getAttribute("data-answer");
    var selection = button.getAttribute("data-choice");
    var choices = quiz.querySelectorAll("[data-choice]");
    var feedback = quiz.querySelector("[data-feedback]");
    var correctFeedback = quiz.getAttribute("data-correct-feedback")
      || "正确：目标序列始终是输入序列向左移动一个 token。";
    var incorrectFeedback = quiz.getAttribute("data-incorrect-feedback")
      || "再看一次序列右移关系：每个位置的目标是紧随其后的 token。";

    choices.forEach(function (choice) {
      var isCorrect = choice.getAttribute("data-choice") === answer;
      choice.classList.toggle("is-correct", selection === answer && isCorrect);
      choice.classList.toggle("is-incorrect", choice === button && !isCorrect);
      choice.disabled = selection === answer;
    });

    if (feedback) {
      feedback.textContent = selection === answer
        ? correctFeedback
        : incorrectFeedback;
    }
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-choice]");
    if (button) {
      answerQuiz(button);
    }
  });
}());
