document.getElementById("formulario").addEventListener("submit", async function(e) {
  e.preventDefault();
  const file = document.getElementById("archivo").files[0];
  if (!file) return alert("Selecciona un archivo .txt");

  const formData = new FormData();
  formData.append("archivo", file);

  const response = await fetch("/validar-placas", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  document.getElementById("resultado").textContent = data.resultado.join("\n");
});

document.addEventListener("DOMContentLoaded", () => {
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
});

function dibujar_universo(matriz) {
    const contenedor = document.getElementById("universo");

    const filas = matriz.tamMatriz.filas;
    const columnas = matriz.tamMatriz.columnas;

    contenedor.style.gridTemplateColumns = `repeat(${columnas}, 30px)`;
    contenedor.innerHTML = "";

    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            const celda = document.createElement("div");
            celda.className = "celda";
            celda.dataset.fila = i;
            celda.dataset.col = j;
            celda.textContent = `${i},${j}`;
            contenedor.appendChild(celda);
        }
    }
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
            });

            const camino = caminosAMostrar[i];
            console.log(`Animando camino ${i + 1}:`, camino);
            
            // Iteramos sobre cada coordenada del camino
            for (let coordenada of camino) {
                const fila = coordenada[1];
                const columna = coordenada[0];
                
                // Calculamos el índice correcto basado en las dimensiones
                const index = fila * matriz.tamMatriz.columnas + columna;
                const celda = contenedor.children[index];
                // console.log(celda);
                
                if (celda) {
                    celda.classList.add("solucion");  
                    celda.classList.add(`camino${i + 1}`); // Añadimos clase específica para cada camino
                    celda.classList.add("actual");
                    await new Promise(resolve => setTimeout(resolve, delay));
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
