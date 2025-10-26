// Confirmación UX al eliminar
function confirmDelete(formEl) {
  const name = formEl?.dataset?.displayName || "este paciente";
  return window.confirm(`¿Seguro que deseas eliminar:\n\n  ${name}\n\nEsta acción no se puede deshacer.`);
}
