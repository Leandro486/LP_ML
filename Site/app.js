const http = require('http');
const express = require('express');
const app = express();


const hostname = 'localhost';
const port = 3000;

const mysql = require('mysql2');

    const connection = mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: 'estgoh',
        database: 'bd'
    });

/*
function conBD(){
    connection.connect((err) =>{
        if(err){
            console.error('Erro ao conectar com a bd: ',err);
            return;
        }
        console.log('Conexão bem sucedida');
        /*
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
*/

function conBD(socialMedia, callback){
    connection.connect((err) =>{
        if(err){
            console.error('Erro ao conectar com a bd: ',err);
            return;
        }
        console.log('Conexão bem sucedida');
        
        const query = `SELECT * FROM tabcomentarios WHERE Social_media = "${socialMedia}"`;

        connection.query(query, (err,results, fields) => {
            if(err){
                console.error('Erro na tabela: ', err);
                return;
            }
           callback(null, results);
        }); 
    });
}


app.get('/executar-conBD/:socialMedia',(req, res) =>{
    const socialMedia = req.params.socialMedia;
    conBD(socialMedia, (err, results) => {
        if (err) {
            res.status(500).send('Erro na consulta ao banco de dados');
        } else {
            res.send(`
            <!DOCTYPE html>
                <html>
                    <head>
                        <title>LP_ML</title>
                        <meta charset="UTF-8">
                        <link rel="stylesheet" type="text/css" href="index.css">
                    </head>
                    <body>
                        <div class="container">
                            <h1>EnergyGreen Fusion</h1>
                            <nav class="nav">
                                <ul>
                                    <li><a href="/">Home</a></li>
                                    <li><a href="/executar-conBD/reddit">Reddit</a></li>
                                    <li><a href="/executar-conBD/facebook">Facebook</a></li>
                                    <li><a href="/executar-conBD/twitter">Twitter</a></li>
                                </ul>
                            </nav>
                        </div>
                        <ul>
                            ${results.map(result => `<li>${result.Text}</li>`).join('')}
                        </ul>
                        <footer>
                            Trabalho Universitário - LP - Leandro D'Água
                        </footer>
                        <style>
                        table {
                            border-collapse: collapse;
                            width: 50%;
                            margin: 20px auto;
                        }
                        th, td {
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                        tr:nth-child(even) {
                            background-color: #f2f2f2;
                        }
                        
                        /* Estilo para o contêiner que envolve o menu */
                        .container {
                            text-align: center;
                        }
                        h1{
                            text-align: center;
                        }
                        
                        /* Estilo para a lista não ordenada (ul) que contém os itens do menu */
                        .nav ul {
                            list-style: none;
                            padding: 0;
                            margin: 0;
                        }
                        
                        /* Estilo para cada item do menu */
                        .nav li {
                            display: inline; /* Para alinhar os itens na mesma linha */
                            margin: 0 15px; /* Espaçamento entre os itens do menu */
                        }
                        
                        /* Estilo para os links do menu */
                        .nav a {
                            text-decoration: none;
                            color: #333; /* Cor do texto do link */
                            font-weight: bold; /* Peso da fonte */
                        }
                        
                        /* Estilo para os links do menu ao passar o mouse sobre eles */
                        .nav a:hover {
                            color: #007BFF; /* Cor do texto ao passar o mouse */
                        }
                        
                        footer {
                            color:black; /* Cor do texto no rodapé */
                            text-align: center; /* Alinhamento de texto no centro */
                            padding: 10px; /* Espaçamento interno */
                        }
                        
                        .hidden{
                            display: none;
                        }
                        </style>
                    </body>
                </html>
            `);
        }
    });
})

const server = http.createServer(app);

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
