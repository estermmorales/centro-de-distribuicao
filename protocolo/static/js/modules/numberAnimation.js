export default function numberAnimation() {
    
    const numerosTotais = document.querySelectorAll(".numero-total");
    numerosTotais.forEach((numeroTotal) => {
    const valorFinal = parseInt(numeroTotal.getAttribute("data-numero"));
    const duracao = 1000;
    const intervalo = 10;

    const incremento = valorFinal / (duracao / intervalo);
    let valorAtual = 0;

    function animarNumero() {
      if (valorAtual < valorFinal) {
        valorAtual += incremento;
        numeroTotal.textContent = Math.round(valorAtual);
        requestAnimationFrame(animarNumero);
      } else {
        numeroTotal.textContent = valorFinal;
      }
    }

    animarNumero();
  });
}