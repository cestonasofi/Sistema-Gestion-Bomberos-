/* ============================================================
   CENTRAL DE BOMBEROS - SCRIPT UNIFICADO
   Todas las páginas cargan este único archivo.
   Cada módulo se inicializa solo si su elemento existe en la página.
   ============================================================ */

// ============================================================
// TEMA OSCURO / CLARO (global)
// ============================================================
function toggleTheme() {
    document.body.classList.toggle('light-mode');
    const isLight = document.body.classList.contains('light-mode');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
}
if (localStorage.getItem('theme') === 'light') {
    document.body.classList.add('light-mode');
}

document.addEventListener("DOMContentLoaded", () => {

    // ============================================================
    // RELOJ EN TIEMPO REAL (Index)
    // ============================================================
    const relojEl = document.getElementById("reloj");
    if (relojEl) {
        function actualizarReloj() {
            const ahora = new Date();
            const dia = String(ahora.getDate()).padStart(2, '0');
            const mes = String(ahora.getMonth() + 1).padStart(2, '0');
            const anio = ahora.getFullYear();
            const horas = String(ahora.getHours()).padStart(2, '0');
            const minutos = String(ahora.getMinutes()).padStart(2, '0');
            const segundos = String(ahora.getSeconds()).padStart(2, '0');
            relojEl.textContent = `${dia}/${mes}/${anio} - ${horas}:${minutos}:${segundos}`;
        }
        setInterval(actualizarReloj, 1000);
        actualizarReloj();
    }

    // ============================================================
    // BUSCADOR EN TIEMPO REAL (Index)
    // ============================================================
    const buscador = document.getElementById('buscador');
    if (buscador) {
        buscador.addEventListener('input', (e) => {
            const termino = e.target.value.toLowerCase().trim();
            document.querySelectorAll('#inventario-completo tbody tr').forEach(fila => {
                const texto = fila.innerText.toLowerCase();
                fila.style.display = texto.includes(termino) ? '' : 'none';
            });
            document.querySelectorAll('#inventario-completo > div').forEach(seccion => {
                const filasVisibles = seccion.querySelectorAll('tbody tr:not([style*="display: none"])');
                seccion.style.display = filasVisibles.length > 0 ? '' : 'none';
            });
        });
    }

    // ============================================================
    // FILTROS POR UNIDAD (Index)
    // ============================================================
    const grupos = document.querySelectorAll('#inventario-completo > div');
    const btns = document.querySelectorAll('#seccion-filtros button');

    function filtrarUnidad(grupo) {
        grupos.forEach(g => {
            g.style.display = (grupo === 'todos' || g.id === 'grupo-' + grupo) ? 'block' : 'none';
        });
        btns.forEach(b => {
            b.style.background = '';
            b.style.color = '';
            b.style.borderColor = '';
        });
        const idBtn = grupo === 'todos' ? 'btn-todos' : 'btn-' + grupo;
        const btnActivo = document.getElementById(idBtn);
        if (btnActivo) {
            btnActivo.style.background = '#c1121f';
            btnActivo.style.color = 'white';
            btnActivo.style.borderColor = '#c1121f';
        }
    }

    if (grupos.length && btns.length) {
        btns.forEach(btn => {
            btn.addEventListener('click', function() {
                const mapa = {
                    'btn-todos': 'todos',
                    'btn-estructural': 'estructural',
                    'btn-rescate': 'rescate',
                    'btn-forestal': 'forestal',
                    'btn-cisterna': 'cisterna',
                    'btn-deposito': 'deposito'
                };
                filtrarUnidad(mapa[this.id] || 'todos');
            });
        });
        filtrarUnidad('todos');
    }

    // ============================================================
    // MODAL DE NOTAS Y CONFIRMACIÓN DE ELIMINAR (Index)
    // ============================================================
    const btnConfirmDelete = document.getElementById('btnConfirmDelete');
    let formToDelete = null;

    window.openNotaModal = function(id, nombre) {
        document.getElementById('modalToolName').innerText = `Herramienta: ${nombre}`;
        document.getElementById('formNota').action = `/herramienta/${id}/nota/`;
        document.getElementById('modalNota').style.display = 'flex';
    };

    window.closeNotaModal = function() {
        document.getElementById('modalNota').style.display = 'none';
    };

    window.confirmDeleteNota = function(form) {
        formToDelete = form;
        document.getElementById('modalConfirmDelete').style.display = 'flex';
        return false;
    };

    window.closeConfirmDelete = function() {
        document.getElementById('modalConfirmDelete').style.display = 'none';
        formToDelete = null;
    };

    if (btnConfirmDelete) {
        btnConfirmDelete.addEventListener('click', function() {
            if (formToDelete) {
                formToDelete.submit();
            }
        });
    }

    // ============================================================
    // CALENDARIO DE INSPECCIONES (Panel de Control / Configuración)
    // ============================================================
    const calendarGrid = document.getElementById('calendarGrid');
    if (calendarGrid) {
        const meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
        const hoy = new Date();
        let calMonth = hoy.getMonth();
        let calYear = hoy.getFullYear();

        // Datos inyectados por el template como JSON
        const datosInspecciones = document.getElementById('datos-inspecciones');
        let inspecciones = {};
        if (datosInspecciones) {
            try {
                inspecciones = JSON.parse(datosInspecciones.textContent);
            } catch (e) {
                console.error('Error al leer los eventos del calendario:', e);
            }
        }

        function renderCalendar() {
            const grid = document.getElementById('calendarGrid');
            const label = document.getElementById('calMonthLabel');
            label.textContent = meses[calMonth] + ' ' + calYear;

            const existingDays = grid.querySelectorAll('.cal-day, .cal-day.empty');
            existingDays.forEach(d => d.remove());

            const primerDia = new Date(calYear, calMonth, 1).getDay();
            const diasEnMes = new Date(calYear, calMonth + 1, 0).getDate();
            const offset = (primerDia + 6) % 7;

            for (let i = 0; i < offset; i++) {
                const empty = document.createElement('div');
                empty.className = 'cal-day empty';
                grid.appendChild(empty);
            }

            for (let d = 1; d <= diasEnMes; d++) {
                const cell = document.createElement('div');
                cell.className = 'cal-day';
                cell.textContent = d;

                const thisDate = new Date(calYear, calMonth, d);
                if (thisDate < new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate())) {
                    cell.classList.add('past');
                }
                if (d === hoy.getDate() && calMonth === hoy.getMonth() && calYear === hoy.getFullYear()) {
                    cell.classList.add('active-day');
                }

                const fechaKey = calYear + '-' + String(calMonth + 1).padStart(2, '0') + '-' + String(d).padStart(2, '0');
                if (inspecciones[fechaKey]) {
                    cell.classList.add('event');
                    cell.title = inspecciones[fechaKey].titulo;
                }

                cell.onclick = function() { selectDate(d); };
                grid.appendChild(cell);
            }
        }

        window.calNav = function(dir) {
            calMonth += dir;
            if (calMonth > 11) { calMonth = 0; calYear++; }
            if (calMonth < 0) { calMonth = 11; calYear--; }
            renderCalendar();
        };

        function selectDate(day) {
            const detail = document.getElementById('calEventDetail');
            const fechaKey = calYear + '-' + String(calMonth + 1).padStart(2, '0') + '-' + String(day).padStart(2, '0');

            if (inspecciones[fechaKey]) {
                const ev = inspecciones[fechaKey];
                detail.innerHTML = '📌 <strong>' + day + ' de ' + meses[calMonth] + ':</strong> ' + ev.titulo +
                    '<div style="margin-top: 8px;">' +
                    `<a href="/evento/${ev.id}/eliminar/" onclick="return confirm('¿Eliminar este evento?');" style="background: #c1121f; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; text-decoration: none; font-weight: bold;">Eliminar</a>` +
                    '</div>';
                detail.style.borderLeftColor = '#f59e0b';
                detail.style.background = 'rgba(245, 158, 11, 0.1)';
            } else {
                detail.innerHTML = '📌 <strong>' + day + ' de ' + meses[calMonth] + ':</strong> Sin inspección programada. Guardia habitual.';
                detail.style.borderLeftColor = '#3b82f6';
                detail.style.background = 'rgba(59, 130, 246, 0.1)';
            }
        }

        renderCalendar();
    }

    // ============================================================
    // CONFIRMAR ENVÍO DE PARTE (Completar Parte)
    // ============================================================
    window.confirmarEnvio = function(form) {
        const marcados = form.querySelectorAll('.select-estado');
        let noDispSinObs = 0;
        marcados.forEach(function (sel) {
            if (sel.value === 'No Disponible') {
                const id = sel.name.replace('estado_', '');
                const obs = form.querySelector('input[name="obs_' + id + '"]');
                if (obs && obs.value.trim() === '') {
                    noDispSinObs++;
                }
            }
        });
        if (noDispSinObs > 0) {
            return confirm('Hay ' + noDispSinObs + ' material(es) marcado(s) como NO DISPONIBLE sin observación. ¿Querés continuar de todas formas?');
        }
        return confirm('¿Enviar el parte y actualizar el inventario? Esta acción quedará registrada.');
    };
});