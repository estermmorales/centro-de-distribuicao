export default function funcionarioEditData() {
    if (window.location.href.includes("funcionarios")) {
        $("tr > td .edit-btn").each(function () {
            $(this).on("click", async function () {
              try {
                const dados = $(this).closest("tr");
                const funcionarioId = dados.find("td:first").text();
          
                const response = await fetch(`/pegar_funcionario/${funcionarioId}`);
                const dadosFuncionario = await response.json();
          
                $('input[name="usuario_id"]').val(dadosFuncionario.usuario);
                $('input[name="nome_editar"]').val(dadosFuncionario.nome);
                $('input[name="email_editar"]').val(dadosFuncionario.email);
                $('input[name="telefone_editar"]').val(dadosFuncionario.telefone);
                $('input[name="documento_editar"]').val(dadosFuncionario.documento);
                $('select[name="permissao_editar"]').val(dadosFuncionario.permissao);
          
                const confirmFuncionario = $("#confirm-funcionario");
                if (confirmFuncionario)
                  confirmFuncionario.html(`<strong>${dadosFuncionario.nome}</strong>`);
              } catch (error) {
                console.error("Erro ao obter dados do funcionário:", error);
              }
            });
          });
    }
}