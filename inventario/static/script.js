document.addEventListener("DOMContentLoaded", () => {
    // === 2. BUSCADOR EN TIEMPO REAL ===
    const buscador = document.getElementById('buscador');
    if (buscador) {
        buscador.addEventListener('input', (e) => {
            const termino = e.target.value.toLowerCase().trim();
            // Filtrar filas de las tablas
            document.querySelectorAll('#inventario-completo tbody tr').forEach(fila => {
                const texto = fila.innerText.toLowerCase();
                fila.style.display = texto.includes(termino) ? '' : 'none';
            });
            // Ocultar tablas que queden vacías
            document.querySelectorAll('#inventario-completo > div').forEach(seccion => {
                const filasVisibles = seccion.querySelectorAll('tbody tr:not([style*="display: none"])');
                seccion.style.display = filasVisibles.length > 0 ? '' : 'none';
            });
        });
    }

    // === 3. FILTROS POR UBICACIÓN ===
    const botonesFiltros = {
        'btn-todos': 'all',
        'btn-estructural': 'grupo-estructural',
        'btn-rescate': 'grupo-rescate',
        'btn-forestal': 'grupo-forestal',
        'btn-cisterna': 'grupo-cisterna',
        'btn-deposito': 'grupo-deposito'
    };

    Object.entries(botonesFiltros).forEach(([idBoton, idGrupo]) => {
        const boton = document.getElementById(idBoton);
        if (boton) {
            boton.addEventListener('click', () => {
                document.querySelectorAll('#inventario-completo > div').forEach(grupo => {
                    grupo.style.display = (idGrupo === 'all' || grupo.id === idGrupo) ? '' : 'none';
                });
            });
        }
    });
});