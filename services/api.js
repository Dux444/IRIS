import axios from "axios";

// Defina o IP fixo que é o seu endereço de rede atual
// Use o IP que aparece na saída do seu servidor: http://192.168.0.6:5000
const YOUR_CURRENT_IP = "192.168.0.6"; 

const api = axios.create({
  // Corrigido para a sintaxe correta de Template Literal (crase `)
  // E apontando para a porta 5000 (API de controle)
  baseURL: `http://${YOUR_CURRENT_IP}:5000`, 
});

export default api;