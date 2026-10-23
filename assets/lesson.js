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
      || "回答正确。";
    var incorrectFeedback = quiz.getAttribute("data-incorrect-feedback")
      || "再想一想：回到上文对照概念，然后重新选择。";

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
