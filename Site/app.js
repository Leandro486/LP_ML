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
