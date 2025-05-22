document.addEventListener("DOMContentLoaded", () => {
    fetch("/lab-interestelar").then(response => response.json()).then(data => {
        // console.log("Datos recibidos:", data);
        const matriz = data.matriz;
        const soluciones = data.soluciones;
        console.log("Soluciones", soluciones)
        dibujar_universo(matriz);
        dibujar_soluciones(soluciones);
    }).catch(error => {
        console.error("Error al cargar los datos:", error);
    })
})

function dibujar_universo(matriz) {
    console.log("Dibujando universo...", matriz);

}

function dibujar_soluciones(matriz) {
    console.log("Dibujando soluciones...", soluciones);
}
