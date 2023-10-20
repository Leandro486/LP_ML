function showTable(tableId) {
    // Esconde todas as tabelas
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        table.classList.add('hidden');
    });

    // Mostra a tabela selecionada
    const selectedTable = document.getElementById(tableId + 'Table');
    selectedTable.classList.remove('hidden');
}