document.addEventListener("DOMContentLoaded", () => {
    fetch("/lab-interestelar")
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);
            const matriz = data.matriz.matriz; // O verifica que esta ruta sea correcta según tu JSON
            console.log(matriz);
            const soluciones = data.soluciones;

            dibujar_universo(matriz);
            animarSolucion(soluciones, matriz); // <-- aquí el cambio
        })
        .catch(error => {
            console.error("Error al cargar los datos:", error);
        });
});

function dibujar_universo(matriz) {
    const contenedor = document.getElementById("universo");
    const filas = matriz.length;
    const columnas = matriz[0].length;

    contenedor.style.gridTemplateColumns = `repeat(${columnas}, 30px)`;
    contenedor.innerHTML = "";

    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            const celda = document.createElement("div");
            celda.className = "celda";
            celda.dataset.fila = i;
            celda.dataset.col = j;
            celda.textContent = matriz[i][j];
            contenedor.appendChild(celda);
        }
    }
}

function animarSolucion(soluciones, matriz, delay = 300) {
  const contenedor = document.getElementById("universo");
  contenedor.querySelectorAll(".celda.solucion").forEach(celda => {
    celda.classList.remove("solucion");
  });

  // Si soluciones es una lista de listas, toma la primera
  const camino = Array.isArray(soluciones[0]) && Array.isArray(soluciones[0][0]) ? soluciones[0] : soluciones;

  async function animar() {
    for (let [fila, col] of camino) {
      const index = fila * matriz[0].length + col;
      const celda = contenedor.children[index];
      if (celda) {
        celda.classList.add("solucion");
      }
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  animar();
}
