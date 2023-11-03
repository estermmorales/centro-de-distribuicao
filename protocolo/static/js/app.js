$(document).ready(function () {
  // Função para ativar o link do menu
  function activeMenuLink() {
    const linksMenu = $(".menu li");

    function handleLink(event) {
      linksMenu.removeClass("active");
      $(this).addClass("active");
    }

    linksMenu.on("click", handleLink);
  }
  activeMenuLink();

  // Função para expandir o menu
  function expandMenu() {
    const sidebar = $(".sidebar");
    const bars = $(".bars");
    const barsIcon = bars.find(".bars-icon");
    const cIcon = bars.find(".c-icon");

    bars.on("click", function () {
      sidebar.toggleClass("active");
      barsIcon.toggleClass("active");
      cIcon.toggleClass("active");
    });
  }
  expandMenu();

  // Lidar com modais
  const triggerButtons = $(".js-modal-button");
  const closeButtons = $(".close");

  triggerButtons.each(function () {
    const target = $(this).data("target");
    const modal = $(`.${target}`);

    $(this).on("click", function () {
      modal.addClass("is-active");
    });
  });

  closeButtons.on("click", function () {
    const target = $(this).data("target");
    const modal = $(`.${target}`);
    modal.removeClass("is-active");
  });

  // Configurando filtros
  const filterButtons = $('.filter');
  filterButtons.each(function () {
      $(this).on('click', function () {
        
          const filter = $(this).data('filter');
          const currentUrl = window.location.href;

          if (currentUrl.includes('?')) {
              // Separa a URL base dos parâmetros de consulta
              const [baseUrl, queryString] = currentUrl.split('?');
              const queryParams = queryString.split('&');

              // Verifica se o filtro específico já existe na URL
              let filterFound = false;

              queryParams.forEach((param, index) => {
                  if (param.startsWith(filter.split('=')[0])) {
                      // Substitua o valor do filtro na URL
                      queryParams[index] = filter;
                      filterFound = true;
                  }
              });

              if (!filterFound) {
                  // Se o filtro não foi encontrado, adiciona-o à URL
                  queryParams.push(filter);
              }

              // Recria a string de consulta com os valores atualizados
              const newQueryString = queryParams.join('&');

              // Atualiza a URL
              window.location.href = `${baseUrl}?${newQueryString}`;
          } else {
              // Se a URL não possui parâmetros de consulta, adiciona o filtro
              window.location.href = `${currentUrl}?${filter}`;
          }
      });
  });


const protocolo = $('input[name="protocolo_id"]');
const emitente = $('input[name="nome_emitente_editar"]');
const destinatario = $('input[name="nome_destinatario_editar"]');
const volumes = $('input[name="qtd_volumes_editar"]');
const situacao = $('select[name="situacao_editar"]');

$('tr > td .edit-btn').each(function() {
  $(this).on('click', function() {
    const dados = $(this).closest("tr");
    protocolo.attr("value", dados[0].cells[0].innerText);
    emitente.attr("value", dados[0].cells[1].innerText);
    destinatario.attr("value", dados[0].cells[2].innerText);
    volumes.attr("value", dados[0].cells[3].innerText);
    situacao.val(dados[0].cells[6].innerText);
  });
});

$("#nome-usuario").autocomplete({
  source: "/autocomplete_usuarios/", 
  messages: {
    noResults: '',
  }
});

});

