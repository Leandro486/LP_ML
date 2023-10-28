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


function conBD(){
    const mysql = require('mysql2');

    const connection = mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: 'estgoh',
        database: 'bd'
    });
    connection.connect((err) =>{
        if(err){
            console.error('Erro ao conectar com a bd: ',err);
            return;
        }
        console.log('Conexão bem sucedida');

        connection.query('SELECT * FROM tabcomentarios', (err, results, fields) => {
            if(err){
                console.error('Erro na tabela: ', err);
                return;
            }

            console.log('Resultados',results);

            connection.end((err) =>{
                if(err){
                    console.error('Erro ao fechar a bd: ',err);
                }else{
                    console.log('Conexão encerrada com sucesso');
                }
            });
        });  
    });
}


conBD();