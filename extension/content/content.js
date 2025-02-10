// Genera un color aleatorio en formato hexadecimal
function generarColorAleatorio() {
    const letras = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letras[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Cambia el color de fondo de la página
document.body.style.backgroundColor = generarColorAleatorio();
