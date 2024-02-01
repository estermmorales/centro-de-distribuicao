export default function getCEP() {
    const cepInput = $('input[name="cep"]');
    const ruaInput = $('input[name="rua"]');
    const bairroInput = $('input[name="bairro"]');
    const cidadeInput = $('input[name="cidade"]');
    const estadoInput = $('input[name="estado"]');
  
    cepInput.on("change", (event) => {
      event.preventDefault();
      let cep = cepInput.val();
      try {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
          .then((response) => response.json())
          .then((body) => {
            ruaInput.val(body.logradouro);
            bairroInput.val(body.bairro);
            cidadeInput.val(body.localidade);
            estadoInput.val(body.uf);
          });
      } catch (error) {
        console.log(error);
      }
    });
}