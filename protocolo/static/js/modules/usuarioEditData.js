export default function usuarioEditData() {
  if (window.location.href.includes("usuarios")) {
    $("tr > td .edit-btn").each(function () {
      $(this).on("click", async function () {
        try {
          const dados = $(this).closest("tr");
          const usuarioId = dados.find("td:first").text();
    
          const response = await fetch(`/pegar_usuario/${usuarioId}`);
          const dadosUsuario = await response.json();
    
          $('input[name="usuario_id"]').val(dadosUsuario.usuario);
          $('input[name="nome_editar"]').val(dadosUsuario.nome);
          $('input[name="email_editar"]').val(dadosUsuario.email);
          $('input[name="telefone_editar"]').val(dadosUsuario.telefone);
          $('input[name="documento_editar"]').val(dadosUsuario.documento);
          $('input[name="cep_editar"]').val(dadosUsuario.cep);
          $('input[name="rua_editar"]').val(dadosUsuario.rua);
          $('input[name="bairro_editar"]').val(dadosUsuario.bairro);
          $('input[name="cidade_editar"]').val(dadosUsuario.cidade);
          $('input[name="estado_editar"]').val(dadosUsuario.estado);
    
          const confirmUsuario = $("#confirm-usuario");
          if (confirmUsuario)
            confirmUsuario.html(`<strong>${dadosUsuario.nome}</strong>`);
        } catch (error) {
          console.error("Erro ao obter dados do usuário:", error);
        }
      });
    });
  }
}