/**
 * TECHSPIRE Learning - Main Client Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alert notifications after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 6000);
  });

  // Quiz Timer Countdown (if timer element exists)
  const timerElem = document.getElementById('quiz-timer');
  if (timerElem) {
    let totalSeconds = parseInt(timerElem.getAttribute('data-seconds'), 10) || 900;
    const quizForm = document.getElementById('quiz-form');

    const interval = setInterval(() => {
      totalSeconds--;
      if (totalSeconds <= 0) {
        clearInterval(interval);
        alert('Time is up! Submitting your assessment automatically.');
        if (quizForm) quizForm.submit();
        return;
      }

      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;
      timerElem.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
      
      if (totalSeconds < 120) {
        timerElem.classList.add('text-danger', 'fw-bold');
      }
    }, 1000);
  }
});
