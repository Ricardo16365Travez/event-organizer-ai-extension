// Escucha el evento cuando se instala la extensión
chrome.runtime.onInstalled.addListener(() => {
    // Crea un elemento en el menú contextual
    chrome.contextMenus.create({
      id: 'sampleContextMenu',
      title: 'Sample Context Menu',
      contexts: ['selection'],
    });
  });
  
  // Escucha los clics en el menú contextual
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'sampleContextMenu') {
      // Realiza una acción cuando se selecciona el menú contextual
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
          alert('¡Has hecho clic en el menú contextual!');
        },
      });
    }
  });
  