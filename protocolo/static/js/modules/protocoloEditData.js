export default function protocoloEditData() {
    if((window.location.href.includes('usuarios')) || (window.location.href.includes('funcionarios')) ) {
        return
    }
    $("tr > td .edit-btn").each(function () {
        $(this).on("click", async function () {
        try {
            const dados = $(this).closest("tr");
            const protocoloId = dados.find("td:first").text();
    
            const response = await fetch(`/pegar_protocolo/${protocoloId}`);
            const dadosProtocolo = await response.json();
    
            $('input[name="protocolo_id"]').val(dadosProtocolo.protocolo);
            $('input[name="nome_emitente_editar"]').val(dadosProtocolo.emitente);
            $('input[name="nome_destinatario_editar"]').val(dadosProtocolo.destinatario);
            $('input[name="qtd_volumes_editar"]').val(dadosProtocolo.volumes);
            $('select[name="situacao_editar"]').val(dadosProtocolo.situacao);
    
            const criado_por = $("#criado-por");
            const confirmProtocolo = $("#confirm-protocolo");
    
            if (criado_por) criado_por.text(`Criado por: ${dadosProtocolo.criadoPor}`);
            if (confirmProtocolo)
            confirmProtocolo.html(`<strong>Protocolo#${dadosProtocolo.protocolo}</strong>`);
        } catch (error) {
            console.error("Erro ao obter dados do protocolo:", error);
        }
        });
    });
}