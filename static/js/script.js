// Confirmación antes de eliminar una tarea y cierre automático de alertas.
document.addEventListener('DOMContentLoaded', function () {
  // Confirmar eliminación
  document.querySelectorAll('.js-confirm-delete').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      const taskTitle = form.getAttribute('data-task-title') || 'esta tarea';
      const confirmed = window.confirm('¿Seguro que deseas eliminar "' + taskTitle + '"? Esta acción no se puede deshacer.');
      if (!confirmed) {
        event.preventDefault();
      }
    });
  });

  // Auto-cerrar las alertas de Django messages después de unos segundos
  document.querySelectorAll('.alert.auto-dismiss').forEach(function (alert) {
    setTimeout(function () {
      alert.classList.remove('show');
      alert.classList.add('fade');
      setTimeout(function () {
        alert.remove();
      }, 300);
    }, 4000);
  });
});
