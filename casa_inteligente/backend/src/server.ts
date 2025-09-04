// src/server.ts
import express from 'express';
import deviceRoutes from './routes/dispositivos'; // Importa as rotas de dispositivo
import roomRoutes from './routes/comodos'; // Importa as rotas de cômodos
import sceneRoutes from './routes/cenas'; // Importa as rotas de cenas
//import { Database } from "./models/Database";

//Database.connect();


const app = express();
const PORT = process.env.PORT || 3000;


app.use(express.json());

// Direciona as requisições para as rotas de dispositivos
app.use('/api/dispositivos', deviceRoutes);

// Direciona as requisições para as rotas de cômodos
app.use('/api/comodos', roomRoutes);

app.use('/api/cenas', sceneRoutes);

app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
    console.log(`Rotas de dispositivos em http://localhost:${PORT}/api/dispositivos`);
    console.log(`Rotas de cômodos em http://localhost:${PORT}/api/comodos`);
    console.log(`Rotas de cenas em http://localhost:${PORT}/api/cenas`)
});