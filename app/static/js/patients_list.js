// Función mejorada de confirmación con modal personalizado
function confirmDelete(formEl) {
  const name = formEl?.dataset?.displayName || "este paciente";
  
  // Crear el modal
  const modal = createDeleteModal(name);
  document.body.appendChild(modal);
  
  // Mostrar modal con animación
  setTimeout(() => modal.classList.add('show'), 10);
  
  // Configurar eventos
  const cancelBtn = modal.querySelector('.modal-btn-cancel');
  const deleteBtn = modal.querySelector('.modal-btn-delete');
  const overlay = modal;
  
  // Función para cerrar modal
  const closeModal = () => {
    modal.classList.remove('show');
    setTimeout(() => {
      if (modal.parentNode) {
        modal.parentNode.removeChild(modal);
      }
    }, 300);
  };
  
  // Event listeners
  cancelBtn.addEventListener('click', closeModal);
  
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      closeModal();
    }
  });
  
  // Evento para confirmar eliminación
  deleteBtn.addEventListener('click', () => {
    closeModal();
    // Enviar el formulario después de cerrar el modal
    setTimeout(() => formEl.submit(), 100);
  });
  
  // Cerrar con ESC
  const handleEscape = (e) => {
    if (e.key === 'Escape') {
      closeModal();
      document.removeEventListener('keydown', handleEscape);
    }
  };
  
  document.addEventListener('keydown', handleEscape);
  
  // Enfocar el botón de cancelar por defecto
  setTimeout(() => cancelBtn.focus(), 100);
  
  // Prevenir el envío del formulario original
  return false;
}

// Función para crear el HTML del modal
function createDeleteModal(patientName) {
  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  
  modal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <div class="modal-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z">
            </path>
          </svg>
        </div>
        <h3 class="modal-title">Confirmar eliminación</h3>
      </div>
      
      <div class="modal-body">
        <p class="modal-text">
          ¿Estás seguro de que deseas eliminar al paciente:
        </p>
        <div class="patient-name">${escapeHtml(patientName)}</div>
        <p class="modal-warning">
          Esta acción no se puede deshacer y se perderán todos los datos del paciente.
        </p>
      </div>
      
      <div class="modal-actions">
        <button type="button" class="modal-btn modal-btn-cancel">
          Cancelar
        </button>
        <button type="button" class="modal-btn modal-btn-delete">
          Eliminar paciente
        </button>
      </div>
    </div>
  `;
  
  return modal;
}

// Función utilitaria para escapar HTML
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
