import initAnimation from "./modules/initAnimation.js";
import activeMenuLink from "./modules/activeMenuLink.js";
import expandMenu from "./modules/expandMenu.js";
import initFilters from "./modules/initFilters.js";
import toggleModals from "./modules/toggleModals.js";
import numberAnimation from "./modules/numberAnimation.js";
import protocoloEditData from "./modules/protocoloEditData.js";
import usuarioEditData from "./modules/usuarioEditData.js";
import funcionarioEditData from "./modules/funcionarioEditData.js";
import getCEP from "./modules/getCEP.js";

$(document).ready(function () {
  //Animação ao carregar a página
  initAnimation()

  // Função para ativar o link do menu
  activeMenuLink();

  // Função para expandir o menu
  expandMenu();

  // Lidar com modais
  toggleModals();

  // Configurando filtros
  initFilters();

  // Animação dos cards dos números dos protocolos
  numberAnimation();

  // Preencher dados do protocolo no modal de edição
  protocoloEditData();

  // Preencher dados do usuário no modal de edição
  usuarioEditData();

  // Preencher dados do usuário no modal de edição
  funcionarioEditData();

  //Preenche CEP do usuário no modal de adição
  getCEP();

});
