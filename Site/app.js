const http = require('http');
const express = require('express');
const app = express();
const mysql = require('mysql2');
const ejs = require('ejs');
app.set('view engine','ejs');

const hostname = 'localhost';
const port = 3000;

let comments = [];
let currentPage = 1;
const commentsPerPage = 10;

const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'estgoh',
    database: 'bd',
    connectionLimit: 10 
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

function conBD(socialMedia, callback) {
    pool.getConnection((err, connection) => {
        if (err) {
            console.error('Erro ao obter conexão do pool: ', err);
            return;
        }
        
        const query = `SELECT * FROM tabcomentarios WHERE Social_media = "${socialMedia}" ORDER BY Date DESC LIMIT 10`;

        connection.query(query, (err, results, fields) => {
            connection.release(); // Libera a conexão de volta para o pool

            if (err) {
                console.error('Erro na tabela: ', err);
                callback(err, null);
            } else {
                comments = results;
                callback(null, results);
            }
        });
    });
}

app.get('/',(req,res) =>{
    res.send(`<!DOCTYPE html>
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
                        <li><a href="/executar-conBD/twitter">Twitter</a></li>
                    </ul>
                </nav>
            </div>
            
            <footer>
                Trabalho Universitário - LP - Leandro D'Água, Rafaela Pereira
            </footer>
            <style>
            h2 {
                text-align:center;
            }
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
    </html>`);
});


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
                                    <li><a href="/executar-conBD/twitter">Twitter</a></li>
                                </ul>
                            </nav>
                        </div>
                        <h2>Comentários Positivos</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Text</th>
                                    <th>Classificação</th>
                                </tr>
                            </thead>
                            <tbody id="tabelaPositivos">
                            ${results.filter(result => result.Classification === 1).map(result => {
                                const formattedDate = new Date(result.Date).toLocaleDateString('pt-BR'); // 'pt-BR' representa o formato brasileiro, ajuste conforme necessário
                                return `
                                    <tr>
                                        <td>${formattedDate}</td>
                                        <td>${result.Text}</td>
                                        <td>${result.Classification}</td>
                                    </tr>
                                `;
                            }).join('')}
                            </tbody>
                        </table>
                        <h2>Comentários Negativos</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Text</th>
                                    <th>Classificação</th>
                                </tr>
                            </thead>
                            <tbody id="tabelaNegativos">
                            ${results.filter(result => result.Classification === 0).map(result => {
                                const formattedDate = new Date(result.Date).toLocaleDateString('pt-BR'); // 'pt-BR' representa o formato brasileiro, ajuste conforme necessário
                                return `
                                    <tr>
                                        <td>${formattedDate}</td>
                                        <td>${result.Text}</td>
                                        <td>${result.Classification}</td>
                                    </tr>
                                `;
                            }).join('')}
                            </tbody>
                        </table>
                        <footer>
                            Trabalho Universitário - LP - Leandro D'Água, Rafaela Pereira
                        </footer>
                        <style>
                        h2 {
                            text-align:center;
                        }
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