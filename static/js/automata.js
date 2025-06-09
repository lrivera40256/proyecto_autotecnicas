let tipoValidacion = 'placa'; // valor por defecto

// Manejar cambios en el tipo de validación
document.querySelectorAll('.toggle-button').forEach(button => {
    button.addEventListener('click', () => {
        // Actualizar botones
        document.querySelectorAll('.toggle-button').forEach(b => b.classList.remove('active'));
        button.classList.add('active');
        
        // Actualizar tipo de validación
        tipoValidacion = button.dataset.type;
        
        // Limpiar resultados
        document.getElementById('resultado').textContent = '';
    });
});

// Manejar envío del formulario
document.getElementById('formulario').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const archivo = document.getElementById('archivo').files[0];
    if (!archivo) {
        alert('Por favor seleccione un archivo');
        return;
    }

    const formData = new FormData();
    formData.append('archivo', archivo);
    formData.append('tipo', tipoValidacion);

    try {
        const response = await fetch('/validar', {
            method: 'POST',
            body: formData
        });
        
        const resultados = await response.json();
        document.getElementById('resultado').textContent = resultados.join('\n');
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('resultado').textContent = 'Error al procesar el archivo';
    }
});