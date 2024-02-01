export default function initFilters() {
    const filterButtons = $(".filter");
    filterButtons.each(function () {
      $(this).on("click", function () {
        const filter = $(this).data("filter");
        const currentUrl = window.location.href;
  
        if (currentUrl.includes("?")) {
          // Separa a URL base dos parâmetros de consulta
          const [baseUrl, queryString] = currentUrl.split("?");
          const queryParams = queryString.split("&");
  
          // Verifica se o filtro específico já existe na URL
          let filterFound = false;
  
          queryParams.forEach((param, index) => {
            if (param.startsWith(filter.split("=")[0])) {
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
          const newQueryString = queryParams.join("&");
  
          // Atualiza a URL
          window.location.href = `${baseUrl}?${newQueryString}`;
        } else {
          // Se a URL não possui parâmetros de consulta, adiciona o filtro
          window.location.href = `${currentUrl}?${filter}`;
        }
      });
    });
  
    let tabela_pesquisa;
    if (window.location.href.includes("funcionarios")) {
      tabela_pesquisa = "funcionario";
    } else {
      tabela_pesquisa = "usuario";
    }
  
    // Autocomplete do campo de pesquisa
    $(".nome-usuario").autocomplete({
      source: "/autocomplete_usuarios/",
      minLength: 2,
      data: {
        tabela: `${tabela_pesquisa}`,
      },
      messages: {
        noResults: "",
      },
    });
  
    $("#search-form").on("submit", function (event) {
      event.preventDefault();
  
      if (window.location.href.includes("usuarios")) {
        this.action = "/usuarios";
      } else if (window.location.href.includes("funcionarios")) {
        this.action = "/funcionarios";
      } else {
        this.action = "/";
      }
  
      this.submit();
    });
}