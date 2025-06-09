document.addEventListener("DOMContentLoaded", () => {
    cargarLaberintoInicial();
});

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload-json', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            console.log("Datos recibidos:", data);
            dibujar_universo(data.matriz);
            animarSolucion(data.soluciones, data.matriz);
        })
        .catch(error => {
            console.error("Error al procesar el archivo:", error);
            alert('Error al procesar el archivo');
        });
    }
}

function cargarLaberintoInicial() {
    fetch("/lab-interestelar")
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);
            const matriz = data.matriz; // O verifica que esta ruta sea correcta según tu JSON
            console.log("Matriz resultante", matriz);
            const soluciones = data.soluciones;
            console.log("Soluciones encontradas", soluciones);

            dibujar_universo(matriz);
            animarSolucion(soluciones, matriz); // <-- aquí el cambio
        })
        .catch(error => {
            console.error("Error al cargar los datos:", error);
        });
}

function dibujar_universo(matriz) {
    const contenedor = document.getElementById("universo");

    const filas = matriz.tamMatriz[1];
    const columnas = matriz.tamMatriz[0];

    contenedor.style.gridTemplateColumns = `repeat(${columnas}, 25px)`;
    contenedor.innerHTML = "";

    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            const celda = document.createElement("div");
            celda.className = "celda";
            celda.dataset.fila = i;
            celda.dataset.col = j;
            
            if (esAgujeroNegro(j, i, matriz.agujerosNegros)) {
                celda.classList.add("agujero-negro");
                celda.innerHTML = '🕳️';
            } else if (esAgujeroGusano(j, i, matriz.agujerosGusano)) {
                celda.classList.add("agujero-gusano");
                celda.innerHTML = '🌀';
            } else if (esEstrellaGigante(j, i, matriz.estrellasGigantes)) {
                celda.classList.add("estrella-gigante");
                celda.innerHTML = '⭐';
            } else if (esZonaRecarga(j, i, matriz.zonasRecarga)) {
                celda.classList.add("zona-recarga");
                celda.innerHTML = '⚡';
            }

            contenedor.appendChild(celda);
        }
    }
}

function esAgujeroNegro(x, y, agujerosNegros) {
    return agujerosNegros.some(agujero => agujero[0] === x && agujero[1] === y);
}

function esAgujeroGusano(x, y, agujerosGusano) {
    return agujerosGusano.some(agujero => agujero[0][0] === x && agujero[0][1] === y);
}

function esEstrellaGigante(x, y, estrellasGigantes) {
    return estrellasGigantes.some(estrella => estrella[0] === x && estrella[1] === y);
}

function esZonaRecarga(x, y, zonasRecarga) {
    return zonasRecarga.some(zona => zona[0] === x && zona[1] === y);
}

function animarSolucion(soluciones, matriz, delay = 300) {
  const contenedor = document.getElementById("universo");
  const MAX_CAMINOS = 5;

  contenedor.querySelectorAll(".celda.solucion").forEach(celda => {
    celda.classList.remove("solucion");
    celda.classList.remove("camino1");
    celda.classList.remove("camino2");
    celda.classList.remove("camino3");
    celda.classList.remove("camino4");
    celda.classList.remove("camino5");
  });

  if (!soluciones || soluciones.length === 0) {
        console.log("No hay soluciones para animar");
        return;
    }

  // Si soluciones es una lista de listas, toma la primera
  const caminosAMostrar = soluciones.slice(0, MAX_CAMINOS);
  console.log(`Mostrando ${caminosAMostrar.length} caminos`);

  async function animar() {
    try {
        // Iteramos sobre cada camino
        for (let i = 0; i < caminosAMostrar.length; i++) {
            contenedor.querySelectorAll(".celda.solucion").forEach(celda => {
                celda.classList.remove("solucion");

                if (celda.querySelector('.rocket')) {
                    celda.querySelector('.rocket').remove();
                }
            });

            const camino = caminosAMostrar[i];
            console.log(`Animando camino ${i + 1}:`, camino);
            
            // Iteramos sobre cada coordenada del camino
            for (let coordenada of camino) {
                const fila = coordenada[1];
                const columna = coordenada[0];
                
                // Calculamos el índice correcto basado en las dimensiones
                const index = fila * matriz.tamMatriz[0] + columna;
                const celda = contenedor.children[index];
                // console.log(celda);
                
                if (celda) {
                    celda.classList.add("solucion");  
                    celda.classList.add(`camino${i + 1}`); // Añadimos clase específica para cada camino
                    celda.classList.add("actual");

                    const contenidoOriginal = celda.innerHTML;

                    celda.innerHTML = '🚀';
                    
                    await new Promise(resolve => setTimeout(resolve, delay));

                    if (coordenada !== camino[camino.length - 1]) {
                        celda.innerHTML = contenidoOriginal;
                    }
                    
                    celda.classList.remove("actual");
                }
            }
        }
    } catch (error) {
        console.error("Error durante la animación:", error);
    }
}

animar();
}
