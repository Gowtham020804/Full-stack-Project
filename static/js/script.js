// Feedback form validation (vanilla)
document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById('feedbackForm');
  if (!form) return;
  form.addEventListener('submit', function(e) {
    const rating = parseInt(form.rating.value || 0, 10);
    const course = form.course.value || "";
    const instructor = form.instructor.value || "";
    if (!course || !instructor) {
      alert("Please select a course and an instructor.");
      e.preventDefault();
      return false;
    }
    if (!(rating >=1 && rating <=5)) {
      alert("Rating must be between 1 and 5.");
      e.preventDefault();
      return false;
    }
    return true;
  });
});
