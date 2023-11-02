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


  const editButtons = document.querySelectorAll('tr > td .edit-btn');
  const emitente = document.querySelector('input[name="nome_emitente"]');
  const destinatario = document.querySelector('input[name="nome_destinatario"]');
  const volumes = document.querySelector('input[name="qtd_volumes"]');
  const situacao = document.querySelector('select[name="situacao"');

  editButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const dados = button.closest("tr")
      emitente.setAttribute("value", dados.cells[3].innerText);
      destinatario.setAttribute("value", dados.cells[4].innerText);
      volumes.setAttribute("value", parseInt(dados.cells[0].innerText));
      situacao.value = dados.cells[5].innerText;
    })
  })

});

